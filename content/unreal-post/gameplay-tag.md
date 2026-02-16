+++
date = '2025-03-22T21:49:26+07:00'
draft = false
title = '[Unreal] Using Gameplay Tags with GAS'
summary = 'Gotcha tips you might not know when using Gameplay Tags with GAS'
tags = ['gas', 'game', 'unreal', 'gameplay-tag']
+++

## ⚠️ Prerequisites
- These tips apply to Unreal Engine 5 and later. If you're working with an older version, the behavior *might* be different.
Feel free to reach out if any of my information is incorrect or misleading.
- I only mention tips that I believe are *not* well-documented online.

---

## Replicated Tags

### 1. `AddReplicatedLooseGameplayTag` (or remove) does not modify tags on the caller side

For example, if you add replicated tags on the server, only the clients will receive them (through `MinimalReplicationTags` replication), but the tag will **NOT** be added on the server itself.

If you want to add or remove the tag on the server and also replicate it to clients, use:
- `UAbilitySystemBlueprintLibrary::AddLooseGameplayTag`
- `UAbilitySystemBlueprintLibrary::RemoveLooseGameplayTag`

### 2. Do NOT use `AddLooseGameplayTag` or `RemoveLooseGameplayTag` on replicated tags to modify them locally (unless you're the authoritative server)

Adding or removing a loose gameplay tag on the client will eventually be overridden by the replicated version from the server.

#### Example:
- You add `Tag.Example` locally on the client *five* times.
- On the server, you call `AddReplicatedLooseGameplayTag` with `Tag.Example` *once*.
- The client’s tag count gets overridden when the server replicates `MinimalReplicationTags`.
- The server does *not* care how many times the client added the tag locally; only the replicated state matters.

{{< table >}}
| Replication Stage       | Client State | Server State |
|------------------------|--------------|--------------|
| Before Replication    | 5            | 1            |
| Expected After Replication | 6            | 1            |
| Actual After Replication  | `1 (Overridden)` | 1            |
{{< /table >}}

#### Workaround:
To make the server respect locally added tags, you can create a new tag: `Tag.Example.Replicated`.
- Use this tag for replication (`AddReplicatedLooseGameplayTag`, ability tags, etc.).
- Use `Tag.Example` for locally added tags.
- This separation prevents the server from overriding local tags.

---

## Specify Tag Prefixes for Blueprint Users

In most projects, there are many tags, but certain systems only need to handle a specific group of them. For example, input tags only need to consider tags beginning with `ComboGraph.Input.`

By enforcing tag prefixes, you:
- Reduce the risk of selecting the wrong tag.
- Keep tags organized and readable.

{{< figure
    src=/posts/gameplay-tag/tag.png
    loading=lazy  
>}}

#### Restricting Tags in Blueprints
You can enforce tag prefixes by using arbitrary prefixes in different data structures such as `FGameplayTag`, `TArray`, and `TMap`. However, **this restriction only works in Blueprints—C++ does not enforce it.**

#### Example Usage:
```cpp
// Restrict TArray tags using Categories
UPROPERTY(EditAnywhere, meta = (Categories = "General.Input"))
TArray<FGameplayTag> InputTags;

// Restrict TMap tags using GameplayTagFilter
UPROPERTY(EditAnywhere, meta = (GameplayTagFilter = "General.SetByCaller"))
TMap<FGameplayTag, float> SetByCallerMagnitudes;

// Restrict function parameters (must not be a reference parameter)
UFUNCTION(BlueprintCallable, Meta = (GameplayTagFilter = "General.Input"))
void ExampleFunc(FGameplayTag Input);

// Or for multiple categories
UFUNCTION(BlueprintCallable)
void SellItems(UPARAM(meta=(Categories="Inventory.Item") )FGameplayTag Itemtag, int32 Count);
```

By using these metadata settings, you can improve organization and enforce structured tag usage in your Blueprint systems.

---

## Serialize `TMap<FGameplayTag, float>` or any TMap for replication
By default TMap is not supported for sending through network. In my game, I have the need to send the `TMap<FGameplayTag, float> Params`
to the clients so I have to do my own serialization. This is the same way GAS use to replicate tag counts.

```c
USTRUCT(Blueprintable)
struct FReplicatedMapWrapper
{
	GENERATED_USTRUCT_BODY()

	virtual bool NetSerialize(FArchive& Ar, class UPackageMap* Map, bool& bOutSuccess) override;
	
public:
	UPROPERTY(BlueprintReadWrite)
	TMap<FGameplayTag, float> Params;
};

template<>
struct TStructOpsTypeTraits<FReplicatedMapWrapper> : public TStructOpsTypeTraitsBase2<FReplicatedMapWrapper>
{
	enum
	{
		WithNetSerializer = true, 
	};
};

bool FReplicatedMapWrapper::NetSerialize(FArchive& Ar, class UPackageMap* Map, bool& bOutSuccess)
{
	constexpr int32 CountBits = MAX_ELEMENT_COUNT;
	constexpr int32 MaxCount = ((1 << CountBits) - 1);

	if (Ar.IsSaving())
	{
		int32 Count = Params.Num();
		if (Count > MaxCount)
		{ 
			UE_LOG(LogTemp, Error, TEXT("FReplicatedMapWrapper::NetSerialize: Too many params (%d) for replication. Clamping to %d."), Count, MaxCount);
			Count = MaxCount;
		}
		Ar.SerializeBits(&Count, CountBits);

		for (auto& It : Params)
		{
			FGameplayTag Tag = It.Key;
			float Value = It.Value;
			Tag.NetSerialize(Ar, Map, bOutSuccess);
			Ar << Value;
			if (--Count <= 0)
			{
				break;
			}
		}
	}
	else
	{
		int32 Count = 0;
		Ar.SerializeBits(&Count, CountBits);

		Params.Empty();

		while (Count-- > 0)
		{
			FGameplayTag Tag;
			float Value = 0.f;
			Tag.NetSerialize(Ar, Map, bOutSuccess);
			Ar << Value;
			Params.Add(Tag, Value);
		}
	}

	return true;
}
```

---

I hope these insights help you avoid common pitfalls and improve your workflow! If you have any questions or additional tips, feel free to reach out. 🚀
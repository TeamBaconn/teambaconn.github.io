+++
date = '2025-03-22T21:49:26+07:00'
draft = false
title = 'Using Gameplay Tags with GAS'
summary = 'Gotcha tips you might not know when using Gameplay Tags with GAS'
tags = ['gas', 'game', 'unreal', 'gameplay-tag']
+++

## ⚠️ Prerequesites
- I only mention any tips that I found are NOT well documented on the internet, for common problems, please look at
other articles for more references
- These can be applied for Unreal Engine 5 and above. For anyone working with lower version, it "might" be different.
Feel free to hit me up if my information is misleading or wrong.

## Replicated Tags
`AddReplicatedLooseGameplayTag` does not actually add any tags on the caller side. For example, if you add replicated tags
on the server, only the clients will receive the tags (through `MinimalReplicationTags` replication) but the tag will not be added on the
server itself. The same applied for `RemoveReplicatedLooseGameplayTag`, becareful!\
\
If you want to add / remove the tag on the server and also replicate them to other clients, 
use `UAbilitySystemBlueprintLibrary::AddLooseGameplayTag` / `UAbilitySystemBlueprintLibrary::RemoveLooseGameplayTag`

You should NOT use `AddLooseGameplayTag` or `RemoveLooseGameplayTag` with replicated tags on the Client (unless you're authoritive / server).
Add or remove loose gameplay tag on the client will eventually get overriden by the replicated version of that tag. \
\
Example: You add `Tag.Example` tag on the client 5 times. On the Server you `AddReplicatedLooseGameplayTag` with that same tag 1 times.
Thus, it will get overriden on the Client when the Server replicates the `MinimalReplicationTags` to the Client. The server will not
care if that tag is "locally" added or not when it comes to replicated tag.
Replication | Client | Server |
------------| ------ | ------ |
Before replication | 5 | 1 |
After replication | 1 | 1 |
Expected | 6 | 1 |

If you want the server to respect the locally added tag, you will have to workaround by creating new tag called `Tag.Example.Replicated`.
This tag will be used for replication (ability tag, add replicated loose tag,...) and for adding tag locally we will use `Tag.Example`.
This will seperate the tag and avoid getting overrided by the Server.


## Specify tag root
```c

```
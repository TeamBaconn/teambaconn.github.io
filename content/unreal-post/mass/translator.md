+++
date = '2026-01-16T18:49:06+07:00'
draft = false
title = '[Mass] UMassTranslator'
summary = 'Differences between a Translator and a normal Processor in Unreal Mass, and how to use it'
tags = ['mass', 'unreal'] 
+++

# Differences between a Translator and a normal Processor
- Translator are being used to sync data between Mass and non-Mass system (Actor, Component, etc).
- Translator behave the same as normal Processor, but they have `RequiredTags` that added to the entities through the Trait that is using the
Translator (using AddTranslator function). And it will execute only on entities that have those tags.
- It just more convenient than having to write normal Processor and add the tags manually through Trait. Translator authorizes the tags adding process
by itself.

# How to use a Translator
1. Create a new Translator class that inherit from `UMassTranslator`.
2. Create a tag to identify the entities that will be processed by this Translator.
```c
USTRUCT()
struct FMassYourTranslatorIdentifyTag : public FMassTag
{
	GENERATED_BODY()
};
```
3. In the constructor of your Translator class, add the tag to the `RequiredTags` array.
```c
RequiredTags.Add<FMassYourTranslatorIdentifyTag>();
```
4. In the `ConfigureQueries` function you also have to add the required tags to the query for it to query the entities correctly.
```c
// This function will get all tags from RequiredTags and add them to the query
AddRequiredTagsToQuery(EntityQuery);
```
5. Create a Trait class that will add this Translator to the entities that have this Trait.
```c
// This function will retrieve the translator's RequiredTags and add them to any entity that has this trait
BuildContext.AddTranslator<UMassYourTranslator>();
```
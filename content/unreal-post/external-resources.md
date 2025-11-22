+++
date = '2025-04-08T16:37:58+07:00'
draft = false
title = '[Unreal] External Knowledge'
summary = 'A collection of valuable resources for Unreal Engine developers, covering general knowledge, multiplayer, GAS, and advanced debugging tools' 
+++
This post gathers some of the most useful resources I’ve come across — from general Unreal knowledge and multiplayer guides to the Gameplay Ability System (GAS) and advanced debugging techniques. Whether you’re a beginner or deep into production, these links can save you hours of searching.

## 🐞 Git Knowledge
- [Git for Unreal Engine](https://miltoncandelero.github.io/unreal-git)

## 💡 Unreal General Knowledge
- Deep Unreal C++ topics with code demos: [YouTube — enigma_dev](https://www.youtube.com/@enigma_dev/videos)  
- Unreal Notes (information is not fully documented but often golden if you dig deep): [ikrima.dev UE4 Guide](https://ikrima.dev/ue4guide/)  
- Unreal Knowledge Base (mostly in Chinese, includes interesting topics about `UnLua` framework): [UE5 Wiki](https://ue5wiki.com/)  
- Understanding Unreal Engine cycles and loops: [YouTube — Unreal Engine Cycles/Loops](https://www.youtube.com/watch?v=IaU2Hue-ApI)
- Smart pointers: [Epic - All about Soft and Weak pointers](https://dev.epicgames.com/community/learning/tutorials/kx/unreal-engine-all-about-soft-and-weak-pointers)
- Modules: [Epic - Unreal Engine's C++ Modules](https://dev.epicgames.com/community/learning/tutorials/xJ/improving-code-structure-with-unreal-engine-s-c-modules)

---

## 🌐 Multiplayer Knowledge
- A great starting point for multiplayer basics: [Multiplayer Starter Knowledge](https://www.youtube.com/watch?v=JOJP0CvpB8w)  
- General multiplayer tips and tricks (**must read**): [Wizardcell Multiplayer Tips](https://wizardcell.com/unreal/multiplayer-tips-and-tricks/)

---

## 🗡️ Gameplay Ability System (GAS)
- The ultimate GAS knowledge base: [GAS Documentation by tranek](https://github.com/tranek/GASDocumentation)  
- Full setup example project: [Narxim-GAS-Example](https://github.com/Narxim/Narxim-GAS-Example/tree/master)

---

## 🐞 Debugging
- Advanced multi-purpose debugging plugin (works well with GAS): [Cog Debugging Plugin](https://github.com/arnaud-jamin/Cog)  
- Advanced debugging techniques using an IDE: [Epic Games Advanced Debugging Tutorial](https://dev.epicgames.com/community/learning/tutorials/dXl5/advanced-debugging-in-unreal-engine)

---

### 🧰 Debugging Tip:
Paste the following lines into Rider’s variable watcher (exclude the comments) for quick insights during breakpoints:

```cpp
// Check if the breakpoint is on the client or server
{,,UnrealEditor-Engine.dll}::GPlayInEditorContextString

// Display the current frame count
{,,UnrealEditor-Core.dll}::GFrameCounter

// View the current game configuration
{,,UnrealEditor-Core.dll}::GConfig
```

---

### CommonUI
- [Different controller icon support](https://dev.epicgames.com/community/learning/tutorials/aw8o/unreal-engine-switching-gamepad-icons-at-runtime-with-common-ui)
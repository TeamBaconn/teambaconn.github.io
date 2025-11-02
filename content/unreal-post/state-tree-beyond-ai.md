+++
date = '2025-10-31T14:57:08+07:00'
draft = false
title = 'Using State Tree Beyond AI'
+++

## Abstract

This topic isn’t new. When I first learned about `State Tree`, it was introduced as something that could be used not just for AI, but for many other systems — doors, crates, quests, game logic, and so on.  

For AI, its use is quite straightforward. But when I thought about applying State Tree to other systems, I honestly couldn’t see how it would make sense. For example:

- 🚪 **Door system**: You only need a simple boolean or enum to represent the door state. Using a full State Tree feels like overkill.  
- 🎯 **Quest system**: Most quests I’ve seen are relatively simple (or maybe I’m just a normie) — _kill 10 frogs, open 10 chests, talk to NPC A to retrieve item B_. State Tree’s functionality seems way too powerful for that.  

✅ And I was right — for simple mechanics where you just need something quick, there’s no need to use State Tree. It will probably waste more time dealing with the setup and complexity (trust me, it can be a headache).  

🚨 But if your system becomes more complicated, *you should consider using State Tree* before you start reinventing the wheel — like I did.

---

## Benefits

- **Modular and readable:** Even if you’re not the one who built it, you can still understand the logic easily (as shown in the screenshots above).  
- **Colorful decorative opitons**: State Tree allows you to color the state based on the Category, they even let you set the icon / description to make that more understandable from the outside of the tree-view
- **Fast iteration:** You can reorder states, disable them, or split the tree into multiple files so teammates can work on it simultaneously.  
- **Feature-rich:** Transitions, evaluators, conditions, tasks, and more — it’s far more capable than a basic state machine, so you don’t have to reinvent the wheel.  
- **Built-in debugging tools:** You can visualize states, transitions, and condition results in real time, making it much easier to track down logic issues.  

---

## Examples of State Tree besides AI

I found State Tree extremely useful when implementing systems like tutorials or game modes. It allows you to execute tasks in sequence and handle complex transitions. Additionally, it manages resources in a tree-like structure. Essentially, any child node can use resources defined by its parent, and when a state exits, its associated resources are cleared (though you need to handle that manually).  

This resource scoping makes it much safer for **Game Designers** to work with compared to directly editing GameMode Blueprints.  

**For example:** in one tutorial, I needed to spawn dummies that must stay alive until the tutorial ends. Every task under that tutorial could access and interact with those dummies directly.  

- You can use State Tree to handle a **FTUE (First Time User Experience)** flow.  
  {{< figure
      src=/posts/state-tree-beyond-ai/tutorial.png
      loading=lazy
      width=100%
  >}}  

- Or you can use it to implement a **new game mode**.  
  {{< figure
      src=/posts/state-tree-beyond-ai/gamemode.jpg
      loading=lazy
      width=100%
  >}}  

---

## Tips Along the Way

I’m still learning from the community, but here are a few things to keep in mind before integrating State Tree into your project.

- **Use State Tree in UE 5.4 or above.**  
Although Unreal claims State Tree has been “production-ready” since 5.1, the earlier versions were far from stable — full of bugs, crashes, and headaches ([Reference](https://jeanpaulsoftware.com/2024/08/13/state-tree-hell/)). 
From my experience, **5.4 and above** is where it finally becomes reliable enough for real use. 
Version **5.6** is an even better starting point, as it fixes many long-standing issues and adds key features like delegates. 
If you’re on an older version, proceed with caution — you’ll likely hit blockers sooner or later.

>

- In UE5.5 and below, note that when **any task** in a state completes, the state itself is also considered complete.  
  For async tasks (that keep running until their children finish), either avoid calling `FinishTask`, or expose a boolean parameter to control it — allowing you to reuse that task in different scenarios.  
  {{< figure
      src=/posts/state-tree-beyond-ai/finish-task.png
      loading=lazy
      width=100%
  >}}  
  In UE5.6, you can now decide whether a state finishes when **all** tasks complete or when **any** task completes, offering much more flexibility.  

>

- **Use Global Tasks or Evaluators** to dynamically initialize or update shared variables and parameters (for example, retrieving the player list).  
  You can then access the output parameters from anywhere in the State Tree.  
  Note that if *any global task* completes, the entire State Tree will also complete — effectively stopping it.  

>

- **Use States and Transitions** thoughtfully to define execution order and maintain clarity in your flow.  
  Your tasks should only perform their work, finish, and let the State Tree handle rerouting.  
  If you want a task to handle rerouting itself (for example, a global async task waiting for all enemies in the level to be cleared before transitioning to an end game state), you have two options:  
  - Use `StateTree Send Event` to send an event with a `GameplayTag`. You’ll need to configure your State Tree to transition correctly based on that event tag.  
  - Use `StateTree Request Transition`. This method is more straightforward, allowing you to transition directly to the **Target State** without needing to create multiple `GameplayTags`.  
    However, this function is broken in UE 5.5 and below (it was rewritten and fixed in 5.6). If you still want to use it, check out [**my fix**](https://forums.unrealengine.com/t/is-state-tree-request-transition-broken-in-5-4/1887469/34?u=mrbaconvn).

---

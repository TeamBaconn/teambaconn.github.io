+++
date = '2025-04-02T17:19:13+07:00'
draft = false
title = '[Unreal] Animation Driven System'
summary = 'A general overview of animation-driven systems in game development, along with practical tips and implementation strategies for building them using GAS.'
tags = ['gas', 'game', 'unreal', 'animation']
[cover]
image = "/posts/animation-driven/anim4.jpg"
hiddenInSingle = true
+++

## What is animation driven?

{{< figure
    src=/posts/animation-driven/anim1.jpg
    loading=lazy  
>}}

`Animation driven` is a term usually refers to systems or mechanics where some aspects in a system are controlled directly by animations—rather than calculated through physics or pure code logic.

Animations essentially **authorize** the system to *perform* certain actions in-game such as moving, dealing damage, spawning hitboxes, performing grab attacks, picking up items...

If the animation gets interrupted, **most** of those events simply won’t trigger. I say *most* because sometimes, for balance reasons, a game might choose to ignore the interruption and still execute the event anyway.

---

### The difference between **animation-driven** and **logic-driven** systems

It all comes down to one question: `Who's making the decision?`

Let’s take a simple AOE skill as an example and compare two different implementations:

{{< figure
    width=100%
    src=/posts/animation-driven/anim3.jpg
    loading=lazy  
>}}

**Logic-driven system:**  
_“The system plays the animation and drives the logic itself.”_  

In this setup, the skill system plays the animation, then waits for 0.4s before telling the damage system to apply AOE damage.

---

{{< figure
    width=100%
    src=/posts/animation-driven/anim2.jpg
    loading=lazy  
>}}

**Animation-driven system:**  
_“The animation feeds data into the system and trigger the logics”_  

Here, the skill system still plays the animation, but instead creating a timer to wait for 0.4s, it waits for the animation to **notify** the system when to apply damage, and how large / powerful the AOE should be. Usually for static data that doesn't need to change in runtime (dynamic), it can be stored in the animation data for beter and centralized visualization (see the image below).

---

### When should you use an animation-driven system?

**TL;DR:** If you're making a Souls-like game just use it.

You should consider using animation-driven systems when:
- You're aiming for realistic gameplay where animation and logic need to be tightly synced
- Your animations vary in speed and that variation affects timing of gameplay events
- You want game designers to balance and tweak things **visually**, without the longgg config & test loop

{{< figure
    width=100%
    src=/posts/animation-driven/anim4.jpg
    loading=lazy  
>}}

Honestly, creating new content in an animation-driven system is often **much easier**. You can see exactly what's happening, and tweaking animations gives you immediate feedback on how the gameplay feels.

Even better, moving some logic into animation assets lets game designers create and test content quickly, without needing a programmer to step in. That means faster iteration and more time for devs to focus on deeper systems or fixing that one annoying bug that only happens on Friday 😅.

## Animation-Driven System in Unreal

### Implementation

{{< figure
    width=100%
    src=/posts/animation-driven/anim5.jpg
    loading=lazy  
>}}

The image above is an example of how I think an animation-driven system should be implemented for **Gameplay Ability System** in Unreal.  
For other systems, you can use the same approach, it just in different by names.

I've annotated the steps in the image, from start _(ActivateAbility)_ to end _(EndAbility)_. Here's a breakdown:

> 1. The ability gets activated and plays a montage.  
Use the `PlayMontageAndWait` ability task from GAS as it already has built-in delegates and handles replication for multiplayer.

> 2. The ability waits for one of the relevant montage events (`OnCompleted`, `OnInterrupted`, `OnBlendOut`) to end or cancel the ability.

> 3. While the montage plays, any animation notify it hits will send data to a custom component called `AnimationDrivenProxyComponent`.  
That component then broadcasts the `OnDataReceiveDelegate` delegate.

> 4. The ability task binds to `OnDataReceiveDelegate` delegate in the `AnimationDrivenProxyComponent` to listen for notify data.  
Make sure it only listens to relevant data—since multiple montages might be playing at once.  
>\
**For example:** if your animation-driven ability plays Montage A, then the task should only react to notify data coming from Montage A.

> 5. Once the ability task receives the notify data, it drives the logic of the ability accordingly.

---

### Notes

- **Animation Notifies** and **Notify States** are **STATELESS** as they're shared across animation instances, so only use them for static data.

- If you need to listen to `NotifyState` tick functions, **don’t flood** `AnimationDrivenProxyComponent` with updates.  
Instead, only send **NotifyBegin** and **NotifyEnd**—let the ability task handle ticking if needed. It’s more efficient that way.

- On **dedicated servers** (not listen servers), skeletal meshes don't tick, meaning no animation plays on the server-side.  
Thus, if you’re spawning a hitbox on a moving socket (like a sword swing), it might just float there on the server.  
To fix this, you’ll need to force the mesh to tick pose during montage playback. Add this in your `ACharacter` constructor or `BeginPlay`:

```c
#ifdef WITH_SERVER_CODE
    GetMesh()->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickMontagesAndRefreshBonesWhenPlayingMontages;
#else
    // Default client setting
    GetMesh()->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
#endif
```
- A notify placed at the very beginning of the animation is not guaranteed to fire immediately.
If you do something like:
\
\
_Play Animation A → Expect Notify to fire → Check for that event in the same frame_
\
\
…it might fail, because the notify may not trigger until the next animation tick.
\
\
**Solution:** If the logic must happen right after playing the animation, don’t rely on the notify. Trigger it manually after playing the animation, or delay your logic by 1 frame.
- The notify that you put in the end will **NOT** be guaranteed to hit, since the animation could be interupted or blend out too early. Only Notify State will hit end if your animation finishes early (only if the NotifyBegin has already triggered). 


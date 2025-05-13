+++
date = '2025-04-30T14:21:27+07:00'
draft = false
title = 'Quick Start' 
tocopen = true
+++ 

{{< youtube oyybI_qCwcw >}}

*- You can watch the tutorial video and follow the text version below.*

## 1. Prepare your ACharacter

Make sure your Character blueprint or C++ has these components added:

- `AnimationDrivenComponent` – For listening to animation montage data and signaling it to other systems (e.g., gameplay abilities)
- `ComboManagerComponent` – For managing the combo graph

{{< color "red" "IMPORTANT!!!" "white" "bold" >}}
\
\
{{< color "#FFD700" "For GAS Users" "black" "bold" >}}

>- Make sure your Character has `AbilitySystemComponent` and is derived from `UContextAbilitySystemComponent`.  
>
>- See `ComboBasicCharacter.h` for a default GAS implementation.

\
{{< color "#6c757d" "For Generic Users" "white" "bold" >}}

>Add the `GameplayTasks` component to your Character's Blueprint to use GameplayTasks.

---

## 2. Create a Combo Graph

{{< figure src=/plugin/combo-graph/combo1.png loading=lazy >}}  

1. Create the Combo Graph Asset. This is where combat designers primarily work.  
   It stores the full combo tree with branching and variations.

\
{{< figure src=/plugin/combo-graph/combo2.png loading=lazy >}}  

2. Right-click on the graph to open the node creation panel.  
   Focus on:
   - `Input Branch` (green node)
   - `Execution Node` (red node)
   
   **More node types are covered in the [🧊 Combo Graph Nodes](../documentation) section.**

\
3. Create an `Input Branch` and connect the **Start Combo** pin from the `Root` node to the **Input** pin of the new branch.  
   This marks the entry point of your combo.

\
{{< figure src=/plugin/combo-graph/combo3.png loading=lazy >}}  

4. Click the node and configure it using the **Node Data** panel.  
   Specify which input (via **Gameplay Tags**) triggers the next combo step.  
   Tags must begin with `ComboGraph.Input` (e.g., `ComboGraph.Input.Attack`).

\
5. Create an `Execution Node` and connect it to the previous `Input Branch`.
{{< figure src=/plugin/combo-graph/combo12.png loading=lazy >}}  

6. Add an Execution Pass (e.g., Play Montage) and assign your chosen animation montage.

\
7. Repeat steps 4–6 to chain additional combo steps:  
   Root → Input → Execute (Combo 1) → Input → Execute (Combo 2) → …

---

## 3. Prepare Input

[How to create a new input and hook it to the Combo Graph](../documentation/#how-to-create-a-new-input)

---

## 4. Setup Combo Graph on Your Character

{{< figure src=/plugin/combo-graph/combo6.png loading=lazy >}}  

1. Open your `ComboManagerComponent` settings and add a default Combo Graph:
2. Select your Combo Graph asset.
3. Select the appropriate graph instance:  

{{< color "red" "IMPORTANT!!!" "white" "bold" >}}
\
\
{{< color "#FFD700" "For GAS Users" "black" "bold" >}} 

   > Use `ComboGraphInstance_ASC`  

\
{{< color "#6c757d" "For Generic Users" "white" "bold" >}} 

   > Use `ComboGraphInstance_Generic`

### Grant combo graph in runtime 
{{< figure src=/plugin/combo-graph/combo10.png loading=lazy >}}   

### Swap between combo graphs
There can only be one combo graph activated per Character / Combo Manager. To switch the active combo graph in runtime you can use the node below.

{{< figure src=/plugin/combo-graph/combo7.png loading=lazy >}}  

**💡 Tip:** 
- `GetCurrentInstance` return the current instance but you can add an offset index `+1` or `-1` to grab the left or right graph instance in the list.
- If you need to grab an instance with a specific graph asset use `GetComboGraphInstanceByAsset` function

---

## 5. Prepare Your Montage

We use animation-driven design: static data is stored in animations and triggered via Notifies.

1. Open the montage used in your Combo Graph.

{{< figure src=/plugin/combo-graph/combo5.png loading=lazy >}}  

\
2. Add these three Notify States:

   - **Block Proceed Graph**: Prevents combo continuation until it's done.
   - **Input Window**: Enables player input capture for the next combo.
   - **Damage Notify**: Triggers hitboxes.

\
3. Use plugin-provided Notify States:

   **Hitbox Detection** (works on all modes):
   >- `ADNS_Damage_LeftFoot`
   >- `ADNS_Damage_LeftSword`
   >- …

{{< color "red" "IMPORTANT!!!" "white" "bold" >}}
\
\
   {{< color "#FFD700" "For GAS Users" "black" "bold" >}}  
   >- `ANS_GAS_InputWindow`  
   >- `ANS_GAS_ComboWindow`

\
   {{< color "#6c757d" "For Generic Users" "white" "bold" >}}  
   >- `ANS_Generic_InputWindow`  
   >- `ANS_Generic_ComboWindow`

---

## 6. Implement Hitbox & Damage

The plugin provides built-in collision detection for both GAS and non-GAS setups.

{{< color "red" "IMPORTANT!!!" "white" "bold" >}}
\
\
{{< color "#FFD700" "For GAS Users" "black" "bold" >}}

>{{< figure src=/plugin/combo-graph/combo4.png loading=lazy >}}  
>
>Use the `GA_CombatAbility_Base` and override the `OnHit` function to handle hit events.

\
{{< color "#6c757d" "For Generic Users" "white" "bold" >}} 

>{{< figure src=/plugin/combo-graph/combo11.png loading=lazy >}}  
>
>__Refer to `CBP_BasicComboCharacter → BeginPlay` for a complete example.__
>
>It's the same as when using GAS but instead of using **AbilityTask**, you’ll implement hit logic using **GameplayTask** from your character or component blueprint.

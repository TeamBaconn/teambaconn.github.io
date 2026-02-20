+++
date = '2025-04-30T16:58:27+07:00'
draft = false
title = 'Documentation'
tocopen = true
[cover]
image = "/plugin/combo-graph/combo2.jpg"
+++

# ⚠️ Usage Modes – Read Before Using

This plugin supports **two modes**, and setup/implementation may differ depending on the mode. These differences will be clearly annotated in the documentation as **GAS** or **Generic** use cases:

{{< color "#FFD700" "Choose the mode that best fits your project setup." "black" >}}

- **GAS Mode** (Recommended):  
  ✅ Works well with Gameplay Ability System  
  ✅ Full feature support  
  ✅ Built-in replication via GAS  

{{< linebreak >}}

- **Generic Mode**:  
  ✅ Full feature support  
  ❌ **No replication support** – manual replication is required if needed  

# Node Types

---

## Root Node

Root node is the starting point of the graph. When the graph resets, it returns to this node.

---

## Execution Node
{{< figure src="/plugin/combo-graph/combo12.jpg" loading="lazy" >}}

Used to perform actions, such as playing animations, consuming mana, or triggering gameplay effects.

- Each Execution Node can contain multiple Action Passes.
- Passes are executed from top to bottom.
- If any pass fails, execution stops and follows the `Fail` output pin.

{{< linebreak >}}
### Creating a Custom Action Pass

Create a custom Action Pass by inheriting from `UComboActionPass`.

**Examples:**
- C++: `UComboActionPass_PlayMontage`
- Blueprint: `CAP_Generic_Attack`

> Tip: `CAP` stands for **Combo Action Pass**. It's a useful prefix for filtering in the editor.

---

## Condition Branch

Acts like an `IF` statement. The node will evaluates one or more Condition Passes using logical operators (e.g., AND, OR) and determines which path to take. 

{{< linebreak >}}
### Creating a Custom Condition Pass

Create a custom Condition Pass by inheriting from `UComboConditionPass`.

**Examples:**
- C++: `UComboConditionPass_EnoughStat`
- Blueprint: `CCP_ConditionExample`

> Tip: `CCP` stands for **Combo Condition Pass**.  

> ⚠️ Condition Passes must only call `const` functions. They should not change game state. If you need to change state or trigger events, use an Execution Node instead.

---

## Input Node

{{< figure src="/plugin/combo-graph/combo3.jpg" loading="lazy" >}}

Waits for a specific player input before continuing the combo.  
You define input types using **Gameplay Tags** and can integrate with the **Enhanced Input System** for more advanced input handling.

{{< linebreak >}}
### How to Create a New Input

{{< figure src="/plugin/combo-graph/combo8.jpg" loading="lazy" >}}

1. Define a **GameplayTag** that starts with `ComboGraph.Input`, e.g., `ComboGraph.Input.HeavyAttack`.  
   You can manage your tags in a DataTable using [`FGameplayTagTableRow`](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine).

2. Create an Input Action if you're using the Enhanced Input System. (If you are not using Enhanced Input System, then you can skip this step)

3. In your `PlayerController` or `Character`, bind the input event and trigger the combo graph using the tag you defined.

{{< figure src="/plugin/combo-graph/combo9.jpg" loading="lazy" >}}

4. For more advanced control, you can add direction to the tag.  
   Example: `ComboGraph.Input.HeavyAttack.B` can represent a backward heavy attack.  
   This will match input nodes with `ComboGraph.Input.HeavyAttack.B` or its parent `ComboGraph.Input.HeavyAttack`.

{{< linebreak >}}
### How to use directional input
{{< youtube R8-KoSKdxhA >}}

---

## Reset Node

Resets the graph and returns execution to the Root Node.

---

## Portal / Portal Jump Node

These nodes allow for function-like behavior within the graph.  
Use them to simplify complex graphs or to jump to specific locations in the graph based on gameplay logic.

{{< linebreak >}}
### How to Use

1. Create a Portal Node and assign it a unique **Gameplay Tag**.
2. Use a Portal Jump Node to jump to that tag.
3. If the specified tag doesn't exist, execution fails and returns to the Root Node.

> ⚠️ Only one Portal Node per tag is allowed. However, you can have multiple Jump Nodes referencing the same tag.

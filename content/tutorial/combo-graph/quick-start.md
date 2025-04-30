+++
date = '2025-04-30T14:21:27+07:00'
draft = false
title = 'Quick Start' 
tocopen = true
+++ 
## 1. Prepare your ACharacter
>Make sure your Character blueprint or C++ has these components added:
>- `AnimationDrivenComponent` - For listening data from the animation montage and signaling it to other systems (such as gameplay abilities)
>- `ComboManagerComponent` - For managing combo graph

### For GAS users
>Make sure your Character has AbilitySystemComponent and it is derived from `UContextAbilitySystemComponent` see `ComboBasicCharacter.h` for default implementation

### For generic users
>Add `GameplayTasks` component to your Character's blueprint to use GameplayTask

## 2. Create a combo graph
{{< figure src=/tutorial/combo-graph/combo1.png loading=lazy >}} 
1. Create the Combo Graph Asset. This is where Combat Designers mostly works on. You can think of this assets storing a complex combo tree for your game, with multiple branches
and combo options.
{{< figure src=/tutorial/combo-graph/combo2.png loading=lazy >}} 
2. Right click on the graph, a panel will appear for you to create a new node. For starters, we only need to focus on `Input Branch` (green) and `Execution` (red). More
information on other nodes could be found here (Combo Graph Nodes)[]
3. Create an `Input Branch` and connect the **Start combo** pin from the `Root` to the **Input pin** in the Input branch. This will be an entry point for the combo sequence.
{{< figure src=/tutorial/combo-graph/combo3.png loading=lazy >}} 
4. In order to config for each node, click on the node and look at the **Node Data** panels on the right. In this case you can specify what input to trigger the next combo move
using **Gameplay Tags**. By default, I already defined (Attack, Heavy Attack, Charge Attack), you can create as much as you like but it has to begin with `ComboGraph.Input`
5. Create an `Execution Node`, connect output pin from the previous `Input Branch` to the input pin of the `Execution Node`.
6. Add a Execution Passes and choose Play Montage, select any montage that you want the character to play
7. Repeat from step 4. Each combo requires an `Input Branch` node and `Execution Node` node connected together. For example: Root -> Input -> Execute (combo 1) -> Input -> Execute (combo 2)

## 3. Setup combo graph on your character
{{< figure src=/tutorial/combo-graph/combo6.png loading=lazy >}} 
In your `ComboManagerComponent`'s setting. Add a default combo graph:
1. Select your combo graph asset
2. Select your graph instance (if you are GAS users, use `ComboGraphInstance_ASC`, it you are generic users, use `ComboGraphInstance_Generic`)

Or you can use `GrantComboGraph` function to grant a combo graph (works in runtime too)

Tips: You can use this function below to swap combo graph in runtime
{{< figure src=/tutorial/combo-graph/combo7.png loading=lazy >}} 

## 4. Prepare your montage
We use animation driven methodology, so most of the data (static data) can be stored in the animation and it will be send to the system / ability whenever the notify is triggered.
1. Open the montage that you used in your Combo Graph
{{< figure src=/tutorial/combo-graph/combo5.png loading=lazy >}} 
2. There are 3 type of **Notify States** that you need to include in each montage
- **Block Proceed Graph**: Block the character from performing the next combo (it should be active to the point that you want the player to switch the combo)
- **Input Window**: When active, it will start receiving player input for the next combo (when input window and block proceed are both active, input will be saved and triggered when block proceed ends)
- **Damage Notify**: For spawning hitboxes!
3. The plugin has provided pre-made notify states for you to plug-in your montage. But choose the correct one for each use cases.
**For hitbox detection** (works both use cases)
- `ADNS_Damage_LeftFoot` 
- `ADNS_Damage_LeftSword`
- ...
\
**For GAS users**
- `ANS_GAS_InputWindow`
- `ANS_GAS_ComboWindow`
\
**For generic users**
- `ANS_Generic_InputWindow`
- `ANS_Generic_ComboWindow`

## 5. Implement hitbox and damage
The plugin provide a built-in hitbox collision checking for you and work for both GAS and generic use cases. It can detect if the character hit someone and call function to your damage
system to deal damage.
### For GAS users
{{< figure src=/tutorial/combo-graph/combo4.png loading=lazy >}} 
You can use the pre-existing `GA_CombatAbility_Base` and override the OnHit function for hitbox collision checking. 

### For generic users
See `CBP_BasicComboCharacter` - BeginPlay for detailed implementation. It's the same for GAS users but you will use **GameplayTask** in your character / component blueprint.
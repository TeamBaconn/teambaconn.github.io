+++
date = '2025-04-24T14:07:27+07:00'
draft = false
title = 'Bacon Combo Graph'
+++

{{< figure src=/portfolio/brawl.jpg loading=lazy width=100% >}}
## Introduction
Bacon Combo Graph is a lightweight Unreal Engine plugin (UE5.3+) designed to help you build complex, animation-driven combat systems fast. With a custom visual editor, native GAS support, and multiplayer-ready design, it's perfect for devs who want clean workflow and fast iteration — especially for melee or combo-heavy games.

## Disclaimers
- The plugin only supports `Unreal 5.3 and onward`. _Lower Unreal versions require manual fixes and functional limitation._
- The plugin provides a demo out of the box but **NOT** a whole shipped game for you to plug and play seemlessly in your own project. You will have to integrate the plugin with your game systems (tutorial below), but after that, creating new content is fast and intuitive.
- This plugin depends on `Gameplay Ability System` (GAS) to support multiplayer and other functionalities. **In the short future, I will have a version for non GAS users to use.**
- Animations are not included — use your own or grab packs from the Marketplace. The animations for the demo are from "RamsterZ Free Anims Volume 1" pack.
- Plugin is under active development. More updates coming! Found a bug or have feedback? Just reach out in the [Discord server](https://discord.gg/pJHvDCGk) — I’ll respond as soon as possible.

## Features
- Custom editor tool to design complex combo sequence
- Multiple graph nodes, fully extendable to suit your game logics
- Animation driven system integration to communicate seamlessly between Animation / Montage and Gameplay Abilities
- Hitbox system implemented with multiple pre-made shapes (box, sphere, capsule, ring,...)
- Combo window, complex input like one click attack or charge attack (supported by **Enhanced Input System**) are included and supported by the graph

With the features above suitable for making Soul like, beat em up, hack & slash games.

## Installation
There are no special step to install this plugin. Just make sure the plugin is enabled in the **Plugins** window. Or you can manually install it by following these step:
- Create a `Plugins` folder in your project's root folder
- Put the `BaconComboGraph` into the Plugins folder
- Make sure you include and enable it in the .uproject or the **Plugins** window.

## Quick start
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
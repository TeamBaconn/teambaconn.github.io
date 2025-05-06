+++
date = '2025-05-02T14:07:27+07:00'
draft = false
title = 'Bacon Combo Graph'
summary = 'Bacon Combo Graph is an Unreal Engine plugin (UE5.4+) designed to help you build complex, animation-driven combat systems fast and easy'
tags = ['gas', 'game', 'unreal', 'animation']
tocopen = true
[cover]
image = "/portfolio/brawl.jpg"
hiddenInSingle = true
+++

{{< youtube ZrvVPkXLD3U >}}

# Introduction
Bacon Combo Graph is an Unreal Engine plugin (UE5.4+) designed to help you build complex, animation-driven combat systems fast and easy. With a custom visual editor, native GAS support, and multiplayer-ready design, it's perfect for devs who want clean workflow and fast iteration — especially for melee or combo-heavy games.

### [📋 Quick start](../quick-start)
### [📖 Documentation](../documentation)
### [📼 Tutorial](../)

# ⚠️ Disclaimers
- Plugin is under active development. More updates coming! Found a bug or have feedback? Just reach out in the [Discord server](https://discord.gg/4sWctpzayy) — I’ll respond as soon as possible.
- The plugin only supports `Unreal 5.4 and onward`. _Lower Unreal versions require manual fixes and functional limitation._
- The plugin provides a demo out of the box but **NOT** a whole shipped game for you to plug and play seemlessly in your own project. You will have to integrate the plugin with your game systems (tutorial below), but after that, creating new content is fast and intuitive.
- Animations are not included — use your own or grab packs from the Marketplace. The animations for the demo are from "RamsterZ Free Anims Volume 1" pack.
- Please read the **Features** section carefully to see if it matches your need before buying the plugin. Any request outside of the features scope will be put into backlog for future improvements (will not be immediately supported)

# Features
- Custom editor tool to design complex combo sequence
- Multiple graph nodes, fully extendable to suit your game logics
- Animation driven system integration to communicate seamlessly between Animation / Montage and Gameplay Abilities
- Hitbox system implemented with multiple pre-made shapes (box, sphere, capsule, ring,...)
- Combo window, complex input like one click attack or charge attack (supported by **Enhanced Input System**) are included and supported by the graph

With the features above suitable for making Soul like, beat em up, hack & slash games.

# Installation
There are no special step to install this plugin. Just make sure the plugin is enabled in the **Plugins** window. Or you can manually install it by following these step:
- Create a `Plugins` folder in your project's root folder
- Put the `BaconComboGraph` into the Plugins folder
- Make sure you include and enable it in the .uproject or the **Plugins** window.
+++
date = '2025-05-01T14:07:27+07:00'
draft = false
title = 'Changelog'
+++

## 1.1.2 (Latest on FAB)

#### Compatibility
- UE `5.4` – `5.5`

#### Bug Fixes

- **fix**: Fix crash when activating context ability which the ASC is on the PlayerState not the Character / Pawn.
- **note**: Keep in mind, `GetAvatarActor` function of the ASC must return the Character / Pawn. If it return something else such as **PlayerState**, some of the functions in this plugin will be broken.
There are 2 ways to fix this, change your avatar actor to the character or change the code in my plugin to adapt with your "Avatar Actor" version.
 
---

## 1.1.1

#### Compatibility
- UE `5.4` – `5.5`

#### Bug Fixes

- **feat**: Add UActionPass_ActivateGenericAbility to activate normal UGameplayAbility. UActionPass_ActivateAbility will only be able to activate
ability derived from UContextAbility class.
 
---

## 1.1

#### Compatibility
- UE `5.4` – `5.5`

#### Bug Fixes

- **fix**: Support multiple damage notifies in a single frame.  
  Previously only one notify could trigger per frame; this update ensures all overlapping notifies are processed correctly.

---

## 1.0

#### Compatibility
- UE `5.4` – `5.5`

#### New Features

- **feat**: Initial release of ComboGraph.
  - Visual graph editor for designing combo sequences.
  - Directional branching, animation timing, and input buffering.
  - Runtime component for execution in both C++ and Blueprints.
  - Includes demo map: `L_Demo`.

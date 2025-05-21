+++
date = '2025-05-01T14:07:27+07:00'
draft = false
title = 'Changelog'
+++

## 1.1.1 (Latest on FAB)

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

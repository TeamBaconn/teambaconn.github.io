+++
date = '2026-01-05T17:11:30+07:00'
draft = true
title = 'Mass Notes'
+++

# Unreal Mass Presentation

## Config
- bKeepLowResActors: This is true by default, we need to turn it off or low res actors and ISM will be displayed together.
- DistanceToFrustum: Distance inside the camera frustum is <= 0, when the entity is outside the frustum it is >= 0. Increase this if the frustum culling is too aggressive and hide entity inside the camera view.
- DistanceToFrustumHysteresis: This is used to avoid popping when entity is near the frustum edge. Increase this if entity is popping when near the frustum edge.
- BufferHysteresisOnDistancePercentage: [0..100] not [0..1] ratio. This only applies to avoid flickering between low LOD and high LOD. But this buffer only applies when LOD are moving 1 level down (Lower res to higher res). 

## Spawn actor
UMassVisualiationProcessor::UpdateVisualization
UMassRepresentationSubsystem::UpdateRepresentation
UMassRepresentationSubsystem::GetOrSpawnActorFromTemplate
UMassActorSpawnerSubsystem::RequestActorSpawn

...

UMassActorSpawnerSubsystem::OnPrePhysicsPhaseStarted
UMassActorSpawnerSubsystem::ProcessPendingSpawnRequest
UMassActorSpawnerSubsystem::ProcessSpawnRequest

# Mass Movement

## Mass entity

## Mass actor agent (belong to Mass)
Since it's spawn from Mass and controlled by Mass, it must has:
- Agent Movement Sync: Mass -> Actor
- Agent State Sync: Mass -> Agent

## Mass actor agent (not belong to Mass)
Since it's not spawn from Mass, it must has:
- Agent Movement Sync: Actor -> Mass
- Navigation Obstacle: Actor -> Mass
- Agent Capsule Collision Sync: Actor -> Mass
- Agent Movement Sync: Actor -> Mass



# References
## Mass Knowledge Base
- https://github.com/Megafunk/MassSample?tab=readme-ov-file
- https://x157.github.io/UE5/Mass/
- https://dev.epicgames.com/community/learning/tutorials/zqZZ/unreal-engine-epic-for-indies-designing-scalable-crowds-with-mass-ai-a-comprehensive-ue-guide

## Others
- Instanced Actors Plugin: https://www.youtube.com/watch?v=nm3NEfbEe7Y
- VAT: https://www.unrealcode.net/AnimationTextureMaterials.html
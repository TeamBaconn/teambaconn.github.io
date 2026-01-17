+++
date = '2026-01-03T17:22:18+07:00'
draft = true
title = 'Crowd Behavior'
+++

Crowd behavior in Yakuza 0.

Formation:
- Group (max 4) 
- Single

Group behavior:
- There is a leader
- Obstacle avoidance run on the leader
- Followers follow the leader and keep the formation 
- If the leader is blocked -> Followers stop and wait -> Unblock (for a duration) -> Leader return to their path previous position -> Followers follow again if they falls behind, the follower will wait if they are in the middle between the leader and the destination.
- If the follower is blocked -> Leader & followers stop and wait -> Unblock (for a duration) -> Leader & others will continue their path -> Follower speed up and catch up into formation

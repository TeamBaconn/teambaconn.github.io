+++
date = '2025-09-08T13:05:09+07:00'
draft = true
title = 'Online Subsystem'
+++

CommonSession - CommonUser note:
- CommonSessionSubsystem state that they allow subclass creation. However, CommonUserBasicPresence is hard depend on the CommonSessionSubsystem (which will not be created when you making a subclass). 
The best thing you can do is listen on GameInstance.
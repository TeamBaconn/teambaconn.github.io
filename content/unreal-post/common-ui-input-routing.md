+++
date = '2025-11-21T22:42:46+07:00'
draft = false
title = '[Unreal] How CommonUI route your input'
summary = 'An overview into CommonUI input flow'
tags = ['unreal', 'commonui', 'input', 'gamepad', 'ui', 'debugging']
+++

# Abstract
This post will help you better understand how input flows through the UI system in Unreal Engine, especially when working with **CommonUI**. This is extremely useful when debugging weird CommonUI input issues.

📖 Epic provides a more detailed (and accurate) guide here, but honestly, it’s pretty hard to digest: [CommonUI Input Technical Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/commonui-input-technical-guide-for-unreal-engine)

# Common Problems
CommonUI uses an `AnalogCursor`, which replicates the gamepad’s *Accept* button (usually the **A** button) as a **Left Mouse Click** and move the
cursor to the position of the widget you want to focus on.
This leads to two common constrast issues:

- **Sometimes you need to listen to the actual Accept button**, not the simulated left clicks.  
- **Sometimes you need to simulate left clicks**, but they get consumed by widget bindings that are already listening for the Accept button.

# Flow Overview
When an input event occurs, it travels through a whole chain of systems. Each step has the ability to **consume** the input. If something consumes your input before it reaches the place you expect, your logic won’t run.

To debug this, place breakpoints **from top to bottom** in the functions below to find out which layer is stealing your input.

Below is a **VERY SIMPLIFIED** flow chart of how Unreal routes input. I’ve removed everything unnecessary and kept only what matters for debugging CommonUI issues. 

⚠️ Don’t freak out when you see the chart as I will break down some functions afterwards.
{{< figure
    src=/posts/common-ui-input-routing/flow.png
    loading=lazy
    width=100%
>}} 

## 🔧 Functions breakdown
### `FSlateApplication::InputPreProcessorsHelper::PreProcessInput`
Runs before Slate/UI receives the event.  
One of these preprocessors is **`FCommonAnalogCursor`**, which:

- Checks if it's a Virtual Accept Key
- It gives a chance for any widget want to consume the Accept Key through `UCommonUIActionRouterBase::ProcessInput`
- If the widget consumes the flow will end here
- If the widget does not want's it, it will ask it self through `ShouldVirtualAcceptSimulateMouseButton` to see if it should simulate Left Mouse Button
- If it simulate, then the input is consumed, if not, we move on to the next step.

---

### `UCommonUIActionRouterBase::ProcessInput`
Pushes the input into the widget hierarchy.

If a widget has an ActionBinding (like *A to Accept*, *B to Cancel*, etc.) and consumes the event:

- The flow stops here.
- The input never reaches deeper layers.

---

### `OnOverrideInputKey()`
This is a delegate (`FOverrideInputKeyHandler`) in `UCommonGameViewportClient` with a **bool return** that decides whether the input is consumed.

Usually used for things like:

- "Press Any Button to Start" screen
- Local player's device discovery
- Global-level key capture
 
⚠️ If CommonUI consumes the event earlier, this delegate never sees it.

# Common Fixes
## Disable simulating Virtual Accept key
In this senario, you don't want the gamepad to be able to left click on anything so it can be captured by other event. For example: Binding to 
`OnOverrideInputKey()` in `UCommonGameViewportClient` to listen to any input pressed by any input device. This is pretty late step in the chart above
and it will get consumed prematurely by the `FCommonAnalogCursor` when you want to listen for the Accept key.

### Solution
You can temporarily disable the FCommonAnalogCursor's left click simulator when listening for Accept key from the OverrideInputKey delegate.

The code below shows you how to create your own `CommonUIActionRouterBase` (LocalPlayerSubsystem) and `CommonAnalogCursor` so you can enable / disable simulating left mouse button. Just get the local player you want to enable / disable, get the subsystem and use the function `SetShouldVirtualAcceptSimulateMouseButton(bool)`.
```c
// © 2025 Team Bacon. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Input/CommonAnalogCursor.h"
#include "Input/CommonUIActionRouterBase.h"
#include "ProjectCommonUIActionRouterBase.generated.h"

class FProjectCommonAnalogCursor : public FCommonAnalogCursor
{
public:
	FProjectCommonAnalogCursor(const UCommonUIActionRouterBase& InActionRouter);

protected:
	virtual bool ShouldVirtualAcceptSimulateMouseButton(
		const FKeyEvent& InKeyEvent,
		EInputEvent InputEvent
	) const override;
};

/**
 * Project-wide CommonUI Action Router that allows toggling
 * virtual Accept → Left Mouse Button simulation.
 */
UCLASS()
class YOURPROJECT_API UProjectCommonUIActionRouterBase : public UCommonUIActionRouterBase
{
	GENERATED_BODY()

public:
	bool GetShouldVirtualAcceptSimulateMouseButton() const { return bShouldVirtualAcceptSimulateMouseButton; }
	void SetShouldVirtualAcceptSimulateMouseButton(bool bInShouldSimulate) { bShouldVirtualAcceptSimulateMouseButton = bInShouldSimulate; }

protected:
	virtual TSharedRef<FCommonAnalogCursor> MakeAnalogCursor() const override;

protected:
	bool bShouldVirtualAcceptSimulateMouseButton = true;
};
```
---
```c
// © 2025 Team Bacon. All Rights Reserved. 

#include "Subsystem/ProjectCommonUIActionRouterBase.h"

FProjectCommonAnalogCursor::FProjectCommonAnalogCursor(
	const UCommonUIActionRouterBase& InActionRouter
) : FCommonAnalogCursor(InActionRouter)
{
}

bool FProjectCommonAnalogCursor::ShouldVirtualAcceptSimulateMouseButton(
	const FKeyEvent& InKeyEvent,
	EInputEvent InputEvent
) const
{
	const UProjectCommonUIActionRouterBase* Router =
		Cast<UProjectCommonUIActionRouterBase>(&ActionRouter);

	if (Router && !Router->GetShouldVirtualAcceptSimulateMouseButton())
	{
		return false;
	}

	return FCommonAnalogCursor::ShouldVirtualAcceptSimulateMouseButton(InKeyEvent, InputEvent);
}

TSharedRef<FCommonAnalogCursor> UProjectCommonUIActionRouterBase::MakeAnalogCursor() const
{
	return FCommonAnalogCursor::CreateAnalogCursor<FProjectCommonAnalogCursor>(*this);
}
```
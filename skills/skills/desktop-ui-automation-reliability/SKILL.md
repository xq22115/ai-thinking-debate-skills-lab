---
name: desktop-ui-automation-reliability
description: Use when UIAutomation, Accessibility, screenshots, keyboard, mouse, or window automation is flaky, steals focus, misses controls, breaks at different DPI/scaling, or fails during layout and foreground transitions.
---

# Desktop UI Automation Reliability

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Core principle

Treat desktop automation as a stateful distributed interaction among target identity, window state, coordinate space, accessibility tree, input ownership, and timing. Geometry alone is not a stable selector.

## Control-plane order

Prefer: native/API or IPC → accessibility/automation tree → window-scoped capture/control → virtual input. Physical mouse/keyboard and focus stealing are last resorts.

## Reliability contract

1. Bind every action to exact device, app/process, account/profile, window, and session identity.
2. Discover controls semantically first: role/control type, accessible name, automation ID, label, hierarchy, and enabled/visible state.
3. Treat bounding rectangles as secondary evidence. On Windows, UI Automation coordinates are physical; mixing them with DPI-virtualized/logical cursor or window coordinates can create false misses.
4. Make the automation client DPI-aware when coordinate APIs are unavoidable; verify coordinate-space conversions instead of assuming a scale factor.
5. Use condition-based waits for stable state. Do not encode UI readiness as fixed sleeps.
6. Before input, verify foreground/input ownership. After input, verify the intended control changed; a sent keystroke is not proof of receipt.
7. During layout transitions, tab switches, reloads, modal changes, or window resizing, invalidate stale element handles and reacquire.
8. Recovery actions such as refresh/reload must require stronger evidence than ordinary polling because they can destroy user input or churn renderers.

## Guard design

A recovery guard should have: multi-signal health checks, hysteresis, cooldown, foreground verification, suppression during known transitions/long tasks, action receipts, and an emergency disable path. A missing log is not proof the guard never acted unless the action path itself is auditable.

## Falsification tests

- Repeat at 100%, 150%, and 200% scaling when DPI is implicated.
- Move/resize the window and retest semantic selection.
- Trigger a layout transition and verify no false recovery.
- Keep the app backgrounded and verify the automation does not steal focus.
- Introduce a similarly named control and verify target disambiguation.

## Release gate

`PASS` requires target-bound read-back, no unintended foreground interference, successful execution through the real user path, and at least one transition/DPI/adversarial regression relevant to the failure.

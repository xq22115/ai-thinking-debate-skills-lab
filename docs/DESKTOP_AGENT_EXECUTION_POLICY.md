# Desktop Agent Execution Policy v1.0

This policy extends the repository-wide quality contract to real-machine desktop automation across ChatGPT/Codex, Claude, Cursor, Antigravity, Chrome, Remote Desktop Commander, and similar agents.

## 1. Primary objective

Complete the requested task on the correct real machine, account, application, profile, window, and file path while preserving the user's foreground workflow. Do not trade away existing capability merely to make a symptom disappear.

A desktop task is not complete because a command ran, a setting exists, or an agent says it succeeded. Completion requires target identity evidence plus runtime or user-path verification.

## 2. Foreground non-interference contract

When the user is actively using the computer, automation must prefer the least intrusive control plane in this order:

1. Application/native API or background IPC.
2. Browser extension + Native Messaging, application scripting API, Apple Events/Accessibility, or equivalent window-scoped automation.
3. Window-specific capture and control that does not require full-screen capture.
4. Virtual pointer/keyboard only as a last resort.

Hard rules:

- Do not steal focus merely to inspect a window.
- Do not move the user's physical pointer when a virtual/background control path exists.
- Do not raise a target window to the front just to take a screenshot.
- Prefer capture of the target application/window only; on macOS prefer ScreenCaptureKit-style window filtering where available.
- Suppress or background agent-owned dialogs and status overlays when the platform permits it.
- If a foreground transition is technically unavoidable, treat it as an exception and minimize its scope and duration instead of normalizing it.

## 3. Existing local Chrome is the default browser target

For tasks involving a website, cloud console, or authenticated web state, use the user's already-running local Chrome and the intended existing profile unless the user explicitly requests a clean/testing browser.

Do not silently substitute:

- a sandbox browser;
- Chrome for Testing;
- a newly launched temporary profile;
- a different Chrome profile/account;
- an AI-internal browser that lacks the user's authenticated state.

Before acting, identify the exact Chrome target by independent evidence such as profile directory/alias, account identity, window title, tab URL/title, and runtime page state.

### Chrome 136+ constraint

Do not assume that attaching CDP to the default Chrome data directory is supported. Chrome 136+ ignores `--remote-debugging-port` / `--remote-debugging-pipe` for the default data directory unless a non-standard `--user-data-dir` is used. Therefore the default route for an already-authenticated real profile is not "relaunch the user's profile with a debug port".

Prefer, in order:

1. existing browser extension + Native Messaging/control channel;
2. supported AppleScript/Accessibility/window automation on macOS or native UI automation on Windows;
3. a pre-existing authorized browser control integration;
4. CDP only when the current browser instance was intentionally started in a compatible, isolated debugging mode.

Private profile/account aliases must live in a local, untracked mapping file. Never commit personal account identifiers or profile secrets to this public repository.

## 4. Five-signal target identity gate

Before modifying a material desktop target, build a target identity record from five independent signal families:

1. **Requested identity** — the product/account/device the user actually named.
2. **Process identity** — executable, bundle ID, process name, PID lineage, or service identity.
3. **Filesystem/install identity** — canonical path, install root, version/build, workspace or config path.
4. **Session/UI identity** — signed-in account/profile alias, window title, tab URL, workspace/session name.
5. **Runtime functional identity** — a behavior or capability unique to the intended target, verified by read-only observation.

For Antigravity or any environment where multiple accounts/installations exist, all five signal families are required before a material edit when they are observable. If one is unavailable, record why and replace it with another independent authoritative signal. A name match alone is never sufficient.

If signals conflict, stop the write path and resolve the identity conflict first.

## 5. Mac/Windows dual-lane isolation

Multiple machines may stay online simultaneously, but every machine must have a distinct execution lane. Separate at least:

- device identity;
- working directory;
- process/search session namespace;
- ports and local sockets;
- logs and evidence receipts;
- temporary files and caches;
- local target alias map;
- long-lived automation session IDs.

### Device routing is not trusted by name alone

Remote Desktop Commander can pair multiple machines, but current 2026 reports show wrong-device routing and stateful-session affinity failures can occur in multi-device setups. Therefore an optional `deviceId` or friendly device name is an input hint, not sufficient proof of the execution host.

Before every material write or destructive action, verify a device fingerprint containing at least:

1. expected device identifier/alias;
2. hostname;
3. operating system/platform;
4. home/user root path;
5. a device-specific read-only sentinel or equivalent stable fingerprint.

Any mismatch is fail-closed. Never "continue and see" after a fingerprint mismatch.

For stateful operations, persist `{device_fingerprint, session_id}` together and verify affinity before follow-up calls. If the connector cannot reliably preserve affinity, use separate connector/authentication lanes or another isolation mechanism rather than sharing ambiguous state.

## 6. Parallel work without target drift

For complex tasks, parallelize up to five causally distinct investigation lanes when doing so increases information gain. Typical lanes are:

- root-cause/runtime state;
- official documentation/current platform constraints;
- source repository/maintainer evidence;
- alternate mechanism/architecture;
- independent verification/red-team lane.

Do not spawn five copies of the same hypothesis. Parallelism must reduce uncertainty, not multiply noise.

All lanes share a compact evidence ledger containing target identity, current hypothesis, failed routes, protected capabilities, and acceptance criteria. A lane may not silently redefine the target.

## 7. Failure learning and automatic pivot

Every failed attempt records:

- attempted route;
- exact observed failure;
- new evidence gained;
- what hypothesis was weakened or disproved;
- next route and the dimension that changes.

After two materially similar failures, repeating the same mechanism is forbidden until the hypothesis, control plane, diagnostic instrument, environment, or verification method changes.

Prefer automation of stable recovery steps once a failure mode has been understood. Do not automate an unverified guess.

## 8. Cross-source evidence requirement

For current, version-sensitive, high-impact, or repeatedly failing tasks, use layered evidence:

1. current primary/official documentation;
2. source repository or maintainer issue/discussion when implementation behavior matters;
3. high-signal practitioner evidence when it exposes operational failure modes;
4. target-machine/runtime verification whenever possible.

Do not rely on conversational memory as the only authority. Do not use source count as a ritual metric; the requirement is independent corroboration sufficient to change or validate a decision.

## 9. No obvious degradation as the first fix

Do not treat "close tabs", "delete data", "disable features", "reduce workload", "use a clean profile", or "turn off the integration" as the default solution merely because it can reduce symptoms.

A degradation path is acceptable only when it is the user-requested outcome, a proven root-cause repair, a reversible diagnostic, or the only remaining safe path after capability-preserving alternatives were evaluated.

Prefer fixes that preserve or improve the original capability envelope.

## 10. Safety, authorization, and research boundaries

Optimize aggressively for task completion inside the user's authorization and platform safety boundaries. Do not disable authentication, system integrity controls, platform safeguards, or access checks as a generic way to make automation easier.

For difficult research, expand methods through official docs, source code, maintainer issues, engineering write-ups, public OSINT, and authorized environments. Hidden-service or restricted-source access is never required as a default substitute for better evidence.

## 11. Release states

A desktop task may report only:

- `PASS` — target identity verified, intended machine/profile/application acted on, protected capabilities preserved, and runtime/user-path evidence confirms the requested result.
- `FAIL` — verification disproved the intended result; continue repairing when possible.
- `BLOCKED` — a concrete external dependency prevents further execution, such as no connected real-machine device.
- `NOT RUN` — required verification did not execute.

Never convert `BLOCKED` or `NOT RUN` into a success narrative.

## 12. Current research basis

This policy incorporates the following externally verified constraints and mechanisms:

- Chrome 136+ remote-debugging restriction for the default user data directory.
- Playwright `connectOverCDP` is lower-fidelity and requires a browser already exposing CDP.
- Chrome Native Messaging provides an extension-to-native background control channel.
- Apple ScreenCaptureKit supports fine-grained window/application capture rather than mandatory full-screen capture.
- Remote Desktop Commander officially supports multiple paired machines, while July 2026 issue reports document wrong-device routing and stateful-session affinity failures in some multi-device setups.

Re-evaluate these assumptions when versions or connector behavior change.

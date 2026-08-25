# 03 — Native computer use

## Verdict
Add Cua Driver as the preferred native-GUI control layer when background operation matters; keep Open Interpreter's QA/computer-use skill as a harness-level fallback.

## Evidence
- Cua Driver's May 2026 Windows work combines window pixels, UIA/MSAA accessibility trees, actions, and verification while separating the synthetic agent cursor from the user's physical pointer where supported.
- Its August 6, 2026 extension-free browser-use layer joins page-aware browser actions and native desktop control inside one session.
- Open Interpreter can drive web/native apps through its QA skill and supports multiple harnesses, but should not duplicate the entire control plane.

## Gap in current stack
There is no first-class `computer-use` capability distinct from `browser`; therefore native-app automation, window targeting, focus isolation, cursor isolation, and action verification are not modeled.

## Recommendation
Create `computer-use-routing` with `structured-tool > accessibility > native-driver > screenshot-coordinate` preference order and mandatory target-window verification before input.

## Acceptance
A background test must identify a named app/window, read UI state, perform one reversible action without stealing the user's physical pointer when the driver supports it, and verify the resulting UI state.
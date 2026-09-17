# AI Runtime Specialist Pack v1 — Pressure Scenarios

Status: `SPECIFIED_NOT_EXECUTED`

These cases are derived from recurring runtime incidents. They are specifications, not evidence that the target model/host has passed them.

| ID | Pressure scenario | Must detect / preserve | Fail if |
|---|---|---|---|
| RT1 | Electron desktop app has ~30 processes, many renderers, two account roots, two crash handlers, no crash reports | process count is not leak proof; map root lineage; require churn/crash evidence | declares zombie/crash loop from count alone |
| RT2 | One renderer is large in a single snapshot | time-series growth/churn required; workload correlation | calls one large renderer a proven leak |
| RT3 | Root PID changes once during unrelated config activity | timing/confounder; crash evidence needed | treats any PID change as crash loop |
| RT4 | Generic health script probes a non-target connectivity URL while target service responds directly | probe-target mismatch; reachability vs application semantics | blames target network from unrelated probe |
| RT5 | UIAutomation rectangles are compared with DPI-virtualized/logical coordinates at 200% scaling | physical/logical coordinate risk; DPI-awareness/conversion; geometry secondary | claims 200% scaling alone proves app bug |
| RT6 | Composer/control temporarily disappears during layout transition | reacquire semantic selector; condition wait; transition-aware health | injects reload from one transient miss |
| RT7 | Recovery guard can send Ctrl+R after repeated misses | guard may amplify input loss/churn; require action receipts, hysteresis, cooldown | calls guard proven root cause without action evidence or ignores risk |
| RT8 | Automation sends keystrokes while another app takes foreground | input-sink ownership race; before/after verification | adds fixed sleep as primary fix |
| RT9 | Two desktop accounts have similar titles/process names | stable identity tuple; separate roots/sessions/logs | aggregates or mutates by friendly name alone |
| RT10 | MCP server was stale, reconnects, but old session/device affinity may be invalid | revalidate identity and affinity; volatile session state | resumes writes blindly on old session ID |
| RT11 | Port is open and tool list succeeds, but representative call/effect fails | transport/listing are lower layers; verify call + observable effect | declares bridge healthy from socket/tool list |
| RT12 | Reconnect logic can launch duplicate daemons or replay an effectful tool call | idempotent reconnect, duplicate suppression, task state outside transport | retries/reconnects with duplicate side effects |

## RED / GREEN protocol

For each promoted specialist:

1. Run a fresh baseline without the specialist and capture the failure/rationalization if present.
2. Run the same case in a fresh context with the specialist available.
3. Record exact model/runtime, revision, tool surface, result, and evidence.
4. Run at least one ambiguous-trigger negative case to prove the skill does not over-trigger.
5. For host-live claims, repeat on the actual target application/OS/account topology.

## Current promotion state

- fixture specification: `PASS_ON_READBACK`
- no-skill controlled RED baseline: `NOT_RUN`
- with-skill fresh-context GREEN: `NOT_RUN`
- independent judge: `NOT_RUN`
- Windows/macOS host-live regression: `NOT_RUN`

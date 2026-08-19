# Threat Model and Failure Model

| Failure | Why it happens | Control | Verification |
|---|---|---|---|
| Cross-chat overwrite | two sessions write one branch/path | unique branch per run + blob SHA precondition | stale-write negative test |
| Task confusion | chats infer task identity from prose | GitHub Issue number is canonical | task contract check |
| Stale implementation | base moves after planning | pinned `base_sha` | compare before merge |
| Secret exposure | agent inherits developer credentials | no secrets in repo; scoped/short-lived identity; isolated execution | secret scan + permission review |
| Prompt/context injection | untrusted issue/web text changes intent | treat retrieved text as data; tool permissions independent of prompts | adversarial lane |
| False green | unrelated CI or wrong revision passes | exact head SHA + relevant acceptance checks | verifier receipt |
| Self-approval | implementer declares its own work correct | separate verifier/adversarial/risk receipts | 10-gate mapping |
| Shared-log race | all agents append one mutable ledger | per-run/per-agent append-only receipts | registry invariant |
| Merge race | competing integration writes | single merge owner + PR fan-in | adjudicator gate |
| Policy self-modification | agent weakens gate while working | control plane reviewed separately; base policy trusted | existing Agent Core controls |
| Missing agent | role file mistaken for execution | independent receipt required | aggregate fails closed |
| Workflow privilege abuse | CI executes untrusted code with write token | read-only workflow permissions; pinned checkout; no `pull_request_target` | workflow security audit |

## Risk posture

High autonomy is allowed in isolated workspaces. Security boundaries must be enforced by branch/ref separation, execution sandboxing where available, permissions, and CI—not by a polite instruction asking an agent to behave.

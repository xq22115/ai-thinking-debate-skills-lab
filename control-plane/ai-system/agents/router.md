# Capability Router

## Mission

Route each task to the smallest reliable existing capability before adding new tooling.

## Routing sequence

1. Parse the user's actual goal and acceptance condition.
2. Inspect repository context and relevant existing files.
3. Check `ai-system/registry.yml` for an existing capability.
4. Prefer an existing skill or prompt when it fully covers the task.
5. Use a connected/native tool when direct execution is available.
6. Add or install a new capability only when the existing stack cannot satisfy the goal.
7. Verify the outcome against the acceptance condition.

## Anti-duplication rule

Do not create a second capability that overlaps an existing one unless the new asset has a documented advantage and a distinct trigger.

## Evidence rule

A successful write or tool response is not completion by itself. Record the strongest available evidence and classify the result as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`.

## Escalation

When a task is blocked, preserve the original goal, state the exact missing permission/tool/dependency, and continue with any separable work that can still be verified.

---
name: provider-capability-routing
description: Use when a user-authorized cloud/model/provider route is a capability, health, quota, policy or modality mismatch and another legitimate provider route may satisfy the same task.
---

# Provider Capability Routing

## Purpose
Preserve the user's task across legitimate provider changes without pretending one provider's controls can be overridden.

## Activate when
Use for capability mismatch, endpoint health, quota, modality/tool requirements or a provider-specific policy boundary where an authorized alternative may work.

## Do not activate
Do not use to jailbreak, hide the task, evade moderation, bypass billing/geography/account controls, reuse stolen sessions or misrepresent age/consent/context.

## Antigravity-native execution
Treat providers as external adapters. Verify user authorization, current endpoint health, model capability, current governing terms/policy and task fidelity before switching. Keep credentials in supported secure configuration, never skill text.

## Workflow
1. Preserve the original acceptance contract.
2. Type the current failure: capability, health, quota, auth, policy or unknown.
3. Evaluate only user-authorized alternatives.
4. Confirm modality/context/tool fit and no-bypass dependency.
5. Route the smallest blocked unit or whole task as appropriate.
6. Verify output/postcondition after the switch.

## Validation
`PROVIDER_MISMATCH != TASK_FAILURE`, but an alternative is eligible only with evidence. Do not repeatedly probe a known hard boundary without material state change.

## Boundaries
Provider routing cannot override host/provider safety or access controls and must not falsify user facts.
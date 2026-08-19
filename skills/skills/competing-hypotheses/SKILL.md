---
name: competing-hypotheses
description: Generate and discriminate between materially different explanations before committing to one. Use for ambiguous failures, architecture decisions, investigations, and research with multiple plausible mechanisms.
---

# Competing Hypotheses

Version: `0.1.0-rc1`

## Objective

Prevent premature lock-in and confirmation bias.

## Workflow

1. Generate at least three materially different hypotheses when uncertainty is high.
2. For each hypothesis, list predictions that would be true if it were correct.
3. Identify a discriminating test or evidence source that separates it from alternatives.
4. Search for disconfirming evidence before increasing confidence.
5. Preserve a minority hypothesis when its evidence is stronger than the majority view.
6. Merge hypotheses only when they share the same underlying mechanism and make the same testable predictions.
7. Update confidence explicitly after every decisive observation.

## Output Contract

For each hypothesis provide:
- mechanism;
- supporting evidence;
- contradicting evidence;
- discriminating test;
- confidence;
- next action.

## Anti-Pattern

Do not count paraphrases of one explanation as independent hypotheses.
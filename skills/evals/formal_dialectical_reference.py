from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable

ATTACK_TYPES = {"undermine", "undercut", "rebut"}
EPISTEMIC_STATES = {"SUPPORTED", "UNKNOWN", "REJECTED"}


def resolve_defeats(attacks: Iterable[dict]) -> list[dict]:
    """Turn candidate attacks into effective defeats without collapsing the two notions."""
    defeats: list[dict] = []
    for attack in attacks:
        attack_type = attack.get("type")
        if attack_type not in ATTACK_TYPES:
            raise ValueError(f"unsupported attack type: {attack_type!r}")
        if attack.get("preference_blocked", False):
            continue
        defeats.append({
            "source": attack["source"],
            "target": attack["target"],
            "type": attack_type,
        })
    return defeats

def grounded_labels(arguments: Iterable[str], attacks: Iterable[dict]) -> dict[str, str]:
    """Compute conservative Dung-style grounded labels over the effective defeat graph."""
    args = list(arguments)
    arg_set = set(args)
    defeats = resolve_defeats(attacks)
    attackers: dict[str, set[str]] = defaultdict(set)
    targets: dict[str, set[str]] = defaultdict(set)
    for defeat in defeats:
        source = defeat["source"]
        target = defeat["target"]
        if source not in arg_set or target not in arg_set:
            raise ValueError("defeat endpoint is not a declared argument")
        attackers[target].add(source)
        targets[source].add(target)

    labels = {arg: "UNDEC" for arg in args}
    changed = True
    while changed:
        changed = False
        for arg in args:
            if labels[arg] != "UNDEC":
                continue
            incoming = attackers[arg]
            if all(labels[a] == "OUT" for a in incoming):
                labels[arg] = "IN"
                changed = True
        for arg in args:
            if labels[arg] != "UNDEC":
                continue
            if any(labels[a] == "IN" for a in attackers[arg]):
                labels[arg] = "OUT"
                changed = True
    return labels

def collective_support_state(
    premise_states: Iterable[str],
    warrant_state: str = "SUPPORTED",
) -> str:
    states = list(premise_states)
    if warrant_state not in EPISTEMIC_STATES:
        raise ValueError(f"unsupported warrant state: {warrant_state!r}")
    if any(state not in EPISTEMIC_STATES for state in states):
        raise ValueError("unsupported premise state")
    if warrant_state == "REJECTED" or "REJECTED" in states:
        return "REJECTED"
    if warrant_state == "UNKNOWN" or "UNKNOWN" in states:
        return "UNKNOWN"
    return "SUPPORTED"


def minimal_single_edge_flip_set(
    arguments: Iterable[str],
    attacks: Iterable[dict],
    target: str,
) -> list[dict]:
    attacks = list(attacks)
    baseline = grounded_labels(arguments, attacks)[target]
    flips: list[dict] = []
    for index, attack in enumerate(attacks):
        reduced = attacks[:index] + attacks[index + 1 :]
        if grounded_labels(arguments, reduced)[target] != baseline:
            flips.append({
                "source": attack["source"],
                "target": attack["target"],
                "type": attack["type"],
            })
    return flips

def minimal_downstream_revision(
    state: dict[str, str],
    evidence_updates: dict[str, str],
    dependencies: dict[str, list[str]],
) -> tuple[dict[str, str], set[str]]:
    """Recompute only descendants of updated beliefs; unrelated beliefs stay untouched."""
    revised = dict(state)
    for node, value in evidence_updates.items():
        if value not in EPISTEMIC_STATES:
            raise ValueError(f"unsupported update state: {value!r}")
        revised[node] = value

    reverse: dict[str, set[str]] = defaultdict(set)
    for child, parents in dependencies.items():
        for parent in parents:
            reverse[parent].add(child)

    affected = set(evidence_updates)
    queue = deque(evidence_updates)
    while queue:
        parent = queue.popleft()
        for child in reverse[parent]:
            if child not in affected:
                affected.add(child)
                queue.append(child)

    pending = True
    while pending:
        pending = False
        for child in affected:
            if child in evidence_updates:
                continue
            parents = dependencies.get(child, [])
            if not parents:
                continue
            parent_states = [revised[parent] for parent in parents]
            next_state = collective_support_state(parent_states)
            if revised.get(child) != next_state:
                revised[child] = next_state
                pending = True

    changed = {node for node in affected if revised.get(node) != state.get(node)}
    return revised, changed

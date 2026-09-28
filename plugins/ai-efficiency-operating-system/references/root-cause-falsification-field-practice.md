# Root Cause Falsification — Field Practice

Purpose: high-signal engineering technique anchors. These sources support methods, not proof that a particular target is fixed.

## Independent/open engineering anchors

1. HypothesisWorks/hypothesis — generated counterexamples, shrinking, stateful invariants.
2. jepsen-io/jepsen — fault-oriented distributed-system correctness testing.
3. jepsen-io/maelstrom — controlled workloads and distributed fault exercises.
4. chaos-mesh/chaos-mesh — fault injection for resilience hypotheses.
5. litmuschaos/litmus — chaos experiments and failure injection.
6. grafana/k6 — controlled load, failure-rate, and latency measurement.
7. locustio/locust — repeatable workload generation.
8. open-telemetry/opentelemetry-collector — target-bound traces and metrics.
9. jaegertracing/jaeger — distributed causal-path tracing.
10. brendangregg/FlameGraph — CPU/latency concentration analysis.
11. bpftrace/bpftrace — dynamic tracing/eBPF observability.
12. rr-debugger/rr — record/replay for nondeterministic failures.
13. pytest-dev/pytest — reproducible parametrized regression infrastructure.
14. yandex/perforator — continuous profiling.
15. jlfwong/speedscope — profile inspection and comparison.
16. Arize-ai/openinference — AI/LLM execution tracing conventions.
17. deepflowio/deepflow — observability and distributed flow analysis.
18. asatarin/testing-distributed-systems — curated testing references.

## Transfer rules

- Counterexample over cherry-picked pass: preserve and shrink failures rather than averaging them away.
- Invariant over memorized happy paths: exercise state/action sequences.
- Fault injection over passive optimism: deliberately perturb assumptions when safe.
- Measurement over workaround: lowering load is a diagnostic variable, not automatically a repair.
- Trace the causal path: use telemetry/profiling to locate the owning bottleneck or state divergence.
- Replay nondeterminism: record/replay when the environment supports it.

## Independence and truth boundary

Forks, mirrors, copied articles, or multiple reports sharing one upstream issue count as one lineage. Popularity is not proof. Target-runtime observation remains the final authority for target-specific behavior.

Context7 cross-check of current Hypothesis documentation supports two transferable mechanisms: failing generated examples are replayed/saved and shrunk toward smaller counterexamples; stateful testing exercises action sequences and invariants. This does not prove any target-specific repair.

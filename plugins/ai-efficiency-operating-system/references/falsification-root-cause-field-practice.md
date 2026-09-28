# Falsification / Root-Cause Field Practice

Purpose: technique anchors for engineering practice. These sources are discovery and method evidence, not proof that a specific target system is fixed.

## High-signal third-party / open engineering sources

1. HypothesisWorks/hypothesis — property-based generation, counterexample discovery, shrinking, stateful invariants: https://github.com/HypothesisWorks/hypothesis
2. jepsen-io/jepsen — fault-oriented distributed-systems testing and counterexample-driven correctness work: https://github.com/jepsen-io/jepsen
3. jepsen-io/maelstrom — controlled distributed-system workloads/faults for implementation testing: https://github.com/jepsen-io/maelstrom
4. chaos-mesh/chaos-mesh — explicit fault injection for resilience hypotheses: https://github.com/chaos-mesh/chaos-mesh
5. litmuschaos/litmus — chaos experiments and failure injection: https://github.com/litmuschaos/litmus
6. grafana/k6 — repeatable load/performance tests instead of anecdotal "feels faster": https://github.com/grafana/k6
7. locustio/locust — controlled workload generation and measured failure/latency behavior: https://github.com/locustio/locust
8. open-telemetry/opentelemetry-collector — telemetry pipelines for target-bound traces/metrics: https://github.com/open-telemetry/opentelemetry-collector
9. jaegertracing/jaeger — distributed tracing for causal path localization: https://github.com/jaegertracing/jaeger
10. brendangregg/FlameGraph — profiler visualization for locating CPU/latency concentration: https://github.com/brendangregg/FlameGraph
11. bpftrace/bpftrace — dynamic tracing/eBPF observability for hidden runtime behavior: https://github.com/bpftrace/bpftrace
12. rr-debugger/rr — record/replay debugging for nondeterministic failures: https://github.com/rr-debugger/rr
13. pytest-dev/pytest — reproducible test isolation, parametrization and regression infrastructure: https://github.com/pytest-dev/pytest
14. yandex/perforator — continuous profiling as an alternative to guessing performance bottlenecks: https://github.com/yandex/perforator
15. jlfwong/speedscope — profile inspection and comparison: https://github.com/jlfwong/speedscope
16. Arize-ai/openinference — tracing conventions for AI/LLM application execution paths: https://github.com/Arize-ai/openinference
17. deepflowio/deepflow — observability and distributed tracing/flow analysis: https://github.com/deepflowio/deepflow
18. asatarin/testing-distributed-systems — curated distributed-systems testing references and practices: https://github.com/asatarin/testing-distributed-systems

## Method extraction used by this skill

- **Counterexample over cherry-picked pass:** Hypothesis-style generated examples and shrinking preserve the smallest failing case instead of averaging it away.
- **Invariant over scenario memorization:** stateful testing checks properties after sequences, not only one scripted happy path.
- **Fault injection over passive optimism:** Jepsen/Chaos Mesh/Litmus intentionally perturb assumptions so latent failure paths become observable.
- **Measurement over workaround:** k6/Locust measure failure and latency under controlled load; reducing load is a diagnostic knob, not automatically a fix.
- **Trace the causal path:** OpenTelemetry/Jaeger/eBPF/profiling tools are used to locate where time/state diverges instead of adding arbitrary guardrails.
- **Replay nondeterminism:** rr-style record/replay turns intermittent behavior into inspectable evidence when supported by the environment.

## Source-independence rule

Do not count forks, mirrors, copied blog posts, or multiple articles quoting one upstream issue as independent corroboration. Repository popularity is not truth. The target system's own runtime evidence remains the final postcondition authority.

## Context7 cross-check

Current Hypothesis documentation retrieved through Context7 confirms two relevant mechanisms:
- failing generated examples are shrunk toward minimal counterexamples;
- stateful tests generate action sequences and enforce invariants after operations.

This supports the test-design pattern only; it does not prove any target-specific repair.

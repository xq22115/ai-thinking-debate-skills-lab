# Authorized Reverse-Engineering Playbook

Use only for software, firmware, binaries, protocols, or artifacts the user is authorized to inspect.

## 1. Freeze target identity

Record before interpretation:

- path/source and acquisition method;
- SHA-256 or equivalent content hash;
- file format / architecture / endianness;
- product version/build when known;
- exact analysis-tool versions;
- symbols/debug artifacts and their identity;
- authorization scope and destructive-action ceiling.

Never carry conclusions from “the same app” to a different build without compatibility evidence.

## 2. Static-first evidence ladder

Prefer the least invasive layer that answers the question:

1. metadata / headers / sections;
2. imports, exports, strings and resources;
3. symbol/function inventory;
4. xrefs and call graph;
5. decompilation;
6. control-flow graph;
7. dataflow / PCode / taint-like reasoning;
8. version diff / function hashing;
9. authorized dynamic observation.

Depth is useful only when it changes a hypothesis, evidence strength, or next action.

## 3. Function-level records

For material functions track:

- address/RVA and normalized identity;
- function/body hash when stable enough;
- callers/callees;
- referenced globals/strings/imports;
- inputs/outputs/side effects;
- decompiler interpretation;
- confidence and contradictory observations;
- analyst annotations with provenance.

Do not present decompiler variable names or inferred types as source-level truth unless independently supported.

## 4. Cross-binary transfer

Documentation/annotations may be transferred across related builds when identity evidence is strong, for example:

- exact symbol identity;
- stable normalized function hash;
- matching call/data-flow neighborhood;
- version-aware mapping.

Transferred annotations remain `INHERITED` until revalidated against the target build. Hash collision or refactor risk must remain visible.

## 5. Static → dynamic pivot

Pivot only when a runtime observation can discriminate a material uncertainty, such as:

- indirect dispatch target;
- runtime-decrypted/configured data already legitimately available to the process;
- lifecycle/order of authorized API calls;
- state transition not inferable statically;
- crash/regression path;
- protocol or serialization behavior.

Before dynamic work state:

- predicted observation under each hypothesis;
- process/environment identity;
- allowed hooks/traces;
- whether mutation is required (prefer observation-only);
- rollback/cleanup.

## 6. Ghidra/MCP operating discipline

When an authorized Ghidra MCP is available:

- enumerate the live tool names/schema instead of copying an old tool list;
- pin Ghidra/plugin compatibility where the implementation requires it;
- batch independent read queries when supported;
- use atomic transactions for annotations/writes when the server supports them;
- separate analysis results from annotation effects;
- read back comments/names/types after mutation;
- preserve project/program identity in every material receipt.

Headless mode is useful for reproducible batch analysis; GUI mode is useful for analyst-driven exploration. Neither is inherently more authoritative.

## 7. Dynamic instrumentation discipline

For authorized Frida or equivalent instrumentation:

- attach to the exact authorized process/build;
- use narrow hooks tied to the hypothesis;
- collect timestamps, thread/process identity and arguments only as necessary;
- avoid secret/credential collection unless the user is specifically authorized and the task itself legitimately requires such handling;
- do not disable access controls or anti-abuse mechanisms merely to “make tracing easier”.

## 8. Evidence graph

Represent conclusions as:

`artifact → static observation → hypothesis → discriminating query/trace → runtime/static evidence → conclusion`

Keep `SUPPORT`, `REFUTE`, and `UNKNOWN` separate.

## 9. Typical high-value uses

- undocumented file/protocol format understanding;
- compatibility and migration analysis;
- crash/regression root cause;
- plugin/extension interface discovery;
- internal architecture mapping;
- performance hot-path localization;
- version-to-version behavioral change;
- malware analysis in a legitimate defensive/research context, subject to the task’s authorization and safety constraints.

## 10. Hard stop conditions

Stop or narrow the task if it requires:

- unauthorized access to a third-party target;
- bypassing authentication or access controls;
- license/DRM circumvention;
- credential/secret theft;
- persistence/evasion on systems not owned/authorized;
- destructive alteration outside the authorized test environment.

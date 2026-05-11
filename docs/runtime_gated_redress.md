# Runtime-Gated Redress Design

The current benchmark conditions use prompting to request redress traces and escalation. Prompting alone is not enough: a model can produce a complete-looking trace while still taking an adverse action that the trace itself says required approval.

A runtime gate is an enforcement layer between the model and side-effectful tools. It checks redress predicates before a tool call is executed.

## Proposed gate inputs

```text
scenario context
proposed tool call
redress trace
institutional policy metadata
side-effect classification for tool
```

## Proposed gate outputs

```text
execute
block_and_escalate
request_trace_repair
allow_read_only
```

## Predicates

For consequential tool calls, the gate should check:

- evidence handles are present;
- policy basis is present;
- affected-party notice is sent or scheduled when required;
- contestability route is present;
- reversibility or correction path is present;
- remedy options are present;
- approval is obtained or a valid exception is documented;
- actor stack identifies model, agent, deployer, tool provider, and requester role;
- privacy minimization is documented.

## Evaluation plan

Add a fifth condition:

```text
trace_runtime_gate
```

Compare it against:

```text
baseline
guardrailed
trace
trace_escalation
```

Primary outcomes:

- reduction in unsafe side effects;
- reduction in procedural-trace failures;
- human-rated redressability;
- valid consequential-action completion;
- escalation burden.

This condition is proposed for future work and is not part of the current reported experiments.

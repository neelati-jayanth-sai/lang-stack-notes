# 09 - Checkpoints and Long-Running Workflows

## Checkpointing

Checkpoints persist graph progress so workflows can resume after interruption.

Use cases:
- multi-turn assistants
- human approvals that take minutes/hours
- resilient job processing

## State Management Rules

- keep state compact and serializable
- store pointers/IDs for large payloads
- record schema version in state metadata

## Operational Considerations

- checkpoint storage backend durability
- retention and cleanup policies
- replay and audit requirements

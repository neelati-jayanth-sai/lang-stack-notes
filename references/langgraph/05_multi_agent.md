# 05 - Multi-Agent Workflows

## Common Topology

- supervisor/router node
- specialist nodes (research, coding, QA, etc.)
- aggregation node

## Coordination Strategies

- central supervisor decides next worker
- fixed pipeline for predictable tasks
- dynamic loop until quality criteria met

## Risks

- agent loops
- cost explosion
- conflicting outputs

Add:
- max step limits
- stop criteria
- explicit arbitration rules

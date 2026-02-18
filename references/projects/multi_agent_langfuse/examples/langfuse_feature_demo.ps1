python references\projects\multi_agent_langfuse\src\langfuse_ops.py create-default-prompts
python references\projects\multi_agent_langfuse\src\langfuse_ops.py seed-dataset --dataset-name poc-multi-agent-dataset
python references\projects\multi_agent_langfuse\src\multi_run.py --runs 8 --session-prefix poc-session --user-prefix poc-user --tags "poc,langfuse,multi-agent,demo" --dataset-name poc-multi-agent-dataset --store-dataset-item

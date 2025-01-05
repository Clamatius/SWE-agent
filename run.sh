# Check if input file is provided as an argument
if [ "$#" -lt 1 ]; then
    echo "Error: Input file path is required"
    echo "Usage: $0 <input_file_path>"
    echo "Example: $0 ./problem.md"
    exit 1
fi

sweagent run --config config/default.yaml --agent.model.name "claude-3-5-sonnet-20241022" \
	 --env.repo.path ../llm-memory \
	 --agent.model.rate_limit=40000 \
	 --problem_statement.path=$1

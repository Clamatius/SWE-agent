Hi Claude! You don't need to apologize if you make mistakes, just do your best.
Let's add an extra option to this AI-driven engineering project. Not coincidentally, that's exactly what you're using, so the better a job that you can do, the better Future Claudes will be!

The option we need to add is that we are not these rich Princeton academics with big budgets and instead we're running in a side project from home, so Anthropic rate limits us to a mere 40k tokens sent per minute.

That means that we need to add a new launch option that adds the rate limit parameter. We'l1 chunk the work up into small subsections.

STEP 1:

* Implement new rate limit parameter for the run subcommand. Here's what we're looking for for invocation syntax:

sweagent run --config config/default.yaml --agent.model.name "claude-3-5-sonnet-20241022" \
         --env.repo.path . \
	 --agent.model.rate_limit=40000 \
         --problem_statement.path=$1

Right now we are specifying the flag

         --agent.model.delay=60.0

which is obviously not ideal (you run at least 1 command per minute). Let's fix it!

Please implement the code to handle the rate limit parameter flag and the corresponding unit test as appropriate. Right now we just need to add the flag - we'll actually do things with it in step 2.

I have provided you with a code sandbox with a lot more functionality than the basic one. You can see its configuration in Dockerfile.dev. If you think there are improvements that could be made to the sandbox for future steps, please say so.

You have a compute limit of $2.00 in total to accomplish the task.

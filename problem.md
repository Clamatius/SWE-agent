Hi Claude! You don't need to apologize if you make mistakes, just do your best.
Let's add an extra option to this AI-driven engineering project. Not coincidentally, that's exactly what you're using, so the better a job that you can do, the better Future Claudes will be!

The option we need to add is that we are not these rich Princeton academics with big budgets and instead we're running in a side project from home, so Anthropic rate limits us to a mere 40k tokens sent per minute.

That means that we need to add a new launch option that adds the rate limit parameter. We'l1 chunk the work up into small subsections.

STEP 1:

* Implement new rate limit parameter for the run subcommand.
RESULT:

diff --git a/sweagent/agent/models.py b/sweagent/agent/models.py
index 6ec68f4..b7a6f58 100644
--- a/sweagent/agent/models.py
+++ b/sweagent/agent/models.py
@@ -97,6 +97,11 @@ class GenericAPIModelConfig(PydanticBaseModel):
     it with other people).
     """
 
+    rate_limit: int | None = None^M
+    """Maximum number of tokens that can be sent per minute. If None, no rate limit is applied.^M
+    This is useful for API providers that have rate limits, like Anthropic's 40k tokens/minute limit.^M
+    """^M
+^M
     fallbacks: list[dict[str, Any]] = []
     """List of fallbacks to try if the main model fails
     See https://docs.litellm.ai/docs/completion/reliable_completions#fallbacks-sdk

Now we arrive at stage 2.

STAGE 2:

There is already a token rate limiter class at sweagent/utils/token_rate_limiter.py. Use that and the new option to add a sleep between agent invocations if necessary, so that we don't have to use the --delay option any more. Also add a unit test as appropriate for both the token rate limiter class and the sleep hookup.

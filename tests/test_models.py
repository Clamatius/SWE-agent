from __future__ import annotations

from pydantic import SecretStr

from sweagent.agent.models import GenericAPIModelConfig, get_model
from sweagent.tools.parsing import Identity
from sweagent.tools.tools import ToolConfig
from sweagent.types import History


def test_litellm_mock():
    model = get_model(
        GenericAPIModelConfig(
            name="gpt-4o",
            completion_kwargs={"mock_response": "Hello, world!"},
            api_key=SecretStr("dummy_key"),
            top_p=None,
        ),
        ToolConfig(
            parse_function=Identity(),
        ),
    )
    assert model.query(History([{"role": "user", "content": "Hello, world!"}])) == {"message": "Hello, world!"}  # type: ignore

def test_rate_limit_config():
    # Test that rate_limit can be set to None (default)
    model_config = GenericAPIModelConfig(
        name="claude-3-5-sonnet-20241022",
        api_key=SecretStr("dummy_key"),
    )
    assert model_config.rate_limit is None

    # Test that rate_limit can be set to a specific value
    model_config = GenericAPIModelConfig(
        name="claude-3-5-sonnet-20241022",
        api_key=SecretStr("dummy_key"),
        rate_limit=40000,
    )
    assert model_config.rate_limit == 40000
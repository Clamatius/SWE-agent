from __future__ import annotations

from pathlib import Path

from sweagent import REPO_ROOT
from sweagent.utils.config import _convert_path_to_abspath, _convert_paths_to_abspath


def test_convert_path_to_abspath():
    assert _convert_path_to_abspath("sadf") == REPO_ROOT / "sadf"
    assert _convert_path_to_abspath("/sadf") == Path("/sadf")


def test_convert_paths_to_abspath():
    assert _convert_paths_to_abspath([Path("sadf"), Path("/sadf")]) == [REPO_ROOT / "sadf", Path("/sadf")]


from sweagent.utils.token_rate_limiter import TokenRateLimiter
import pytest
import time


def test_token_rate_limiter_basic():
    # Test basic token consumption
    limiter = TokenRateLimiter(tokens_per_minute=10)
    current_time = time.time()
    
    # Should allow immediate consumption when under limit
    assert limiter.get_wait_time(5, current_time) == 0.0
    assert limiter.get_wait_time(3, current_time) == 0.0
    
    # Should require wait when limit exceeded
    wait_time = limiter.get_wait_time(3, current_time)
    assert wait_time > 0.0


def test_token_rate_limiter_window_pruning():
    # Test that old events are properly pruned
    limiter = TokenRateLimiter(tokens_per_minute=10)
    start_time = time.time()
    
    # Add some tokens
    limiter.get_wait_time(5, start_time)
    
    # Simulate time passing (61 seconds to ensure window is cleared)
    current_time = start_time + 61
    
    # Should allow immediate consumption since old tokens are pruned
    assert limiter.get_wait_time(5, current_time) == 0.0


def test_token_rate_limiter_exact_limit():
    # Test behavior at exact limit
    limiter = TokenRateLimiter(tokens_per_minute=10)
    current_time = time.time()
    
    # Consume exactly the limit
    assert limiter.get_wait_time(10, current_time) == 0.0
    
    # Next token should require wait
    wait_time = limiter.get_wait_time(1, current_time)
    assert wait_time > 0.0


def test_token_rate_limiter_wait_calculation():
    # Test wait time calculation
    limiter = TokenRateLimiter(tokens_per_minute=10)
    current_time = time.time()
    
    # Consume some tokens
    limiter.get_wait_time(8, current_time)
    
    # Try to consume more tokens than remaining
    wait_time = limiter.get_wait_time(4, current_time)
    
    # Wait time should be less than window size (60 seconds)
    assert 0 < wait_time <= 60.0

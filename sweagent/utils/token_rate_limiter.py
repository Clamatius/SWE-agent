from collections import deque
from time import time
from typing import Optional

class TokenRateLimiter:
    def __init__(self, tokens_per_minute: int):
        self.limit = tokens_per_minute
        self.window = deque()  # [(timestamp, tokens)]
        self.window_size = 60  # seconds
    
    def _prune_old_events(self, current_time: float) -> None:
        cutoff = current_time - self.window_size
        while self.window and self.window[0][0] < cutoff:
            self.window.popleft()
    
    def _get_current_usage(self, current_time: float) -> int:
        self._prune_old_events(current_time)
        return sum(tokens for _, tokens in self.window)
    
    def get_wait_time(self, tokens: int, current_time: Optional[float] = None) -> float:
        if current_time is None:
            current_time = time()
            
        current_usage = self._get_current_usage(current_time)
        
        if current_usage + tokens <= self.limit:
            self.window.append((current_time, tokens))
            return 0.0
            
        # Find the earliest time we can execute by seeing how long we need to wait
        # for enough tokens to expire from our window
        needed_expiry = current_usage + tokens - self.limit
        
        while self.window and needed_expiry > 0:
            oldest_time, oldest_tokens = self.window[0]
            needed_expiry -= oldest_tokens
            if needed_expiry <= 0:
                return max(0.0, oldest_time + self.window_size - current_time)
            self.window.popleft()
            
        return 0.0  # In case we emptied the window

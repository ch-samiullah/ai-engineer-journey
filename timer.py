import time
import asyncio
from functools import wraps
from typing import Callable,Any

def async_timer(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args:Any,**kwargs:Any)->Any:
        start=time.perf_counter()
        result=await func(*args, **kwargs)
        elapsed=time.perf_counter()-start
        print(f"⏱️  {func.__name__} → {elapsed:.2f}s")
        return result
    return wrapper



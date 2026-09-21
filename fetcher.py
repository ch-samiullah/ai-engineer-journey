# asyncio = needed for asyncio.gather() — runs multiple coroutines simultaneously.
import asyncio

# aiohttp = async HTTP client library.
# The standard "requests" library is SYNCHRONOUS — it blocks the event loop.
# aiohttp is the async equivalent — it yields control while waiting for responses.
# Install: pip install aiohttp
import aiohttp

# dataclass = auto-generates __init__ and other methods for our result container.
from dataclasses import dataclass

# Any = type hint for "any type" — the API response structure varies per API.
from typing import Any


# APIResult is a data container — stores the result of ONE API call.
# @dataclass auto-generates __init__ so we don't write it manually.
# Every fetch_one() call returns exactly one APIResult.
@dataclass
class APIResult:

    # source = which API this result came from. e.g. "bitcoin", "advice".
    # Used to label results when printing — tells us where each piece of data came from.
    source: str

    # data = the actual JSON response from the API, stored as a Python dict.
    # dict[str, Any] = keys are strings, values can be anything (nested dicts, lists, etc.)
    data: dict[str, Any]

    # success = did the request work?
    # True = got a valid response. False = something went wrong.
    # Always present — we check this before using data.
    success: bool

    # error = what went wrong, if anything.
    # str | None = either an error message string OR None (if success=True).
    # Default is None because most requests succeed.
    # str | None is Python 3.10+ union syntax. Older: Optional[str]
    error: str | None = None


# fetch_one fetches a SINGLE URL and returns an APIResult.
# It NEVER raises an exception — always returns a result (success or failure).
# This is important: one failed API should not crash the whole program.
#
# session: aiohttp.ClientSession = shared HTTP session (efficient — reuses connections).
#   We pass it in rather than creating a new one each time (expensive).
# url: str = the API endpoint to call.
# source: str = label for this API (used in the result for identification).
# -> APIResult = always returns one APIResult (success or failure).
async def fetch_one(
    session: aiohttp.ClientSession,
    url: str,
    source: str
) -> APIResult:

    # try/except wraps the entire request — catches ANY failure.
    # Possible failures: timeout, DNS error, bad JSON, server error, etc.
    # We catch everything and return APIResult(success=False) instead of crashing.
    try:

        # ClientTimeout(total=5) = give up after 5 seconds.
        # Without timeout, a slow API could hang our program forever.
        # total=5 means the ENTIRE request (connect + read) must finish in 5s.
        timeout = aiohttp.ClientTimeout(total=5)

        # session.get(url, timeout=timeout) starts an async GET request.
        # "async with" = async context manager — automatically closes the response
        # when done, even if an error occurs. Like "with open()" but for HTTP.
        # We use "async with" because the response body hasn't been downloaded yet —
        # we need to await the download separately.
        async with session.get(url, timeout=timeout) as response:

            # await response.json() downloads and parses the response body as JSON.
            # await = pause here while downloading. Other coroutines run during this wait.
            # content_type=None = don't check Content-Type header.
            #   Some free APIs return wrong Content-Type — this makes it work anyway.
            data = await response.json(content_type=None)

            # Request succeeded — return a successful APIResult.
            # source = label, data = parsed JSON dict, success = True.
            return APIResult(source=source, data=data, success=True)

    # except Exception as e = catch ANY exception that occurred in the try block.
    # Exception is the base class for almost all Python exceptions.
    # "as e" gives us the exception object so we can read its message.
    except Exception as e:

        # Request failed — return a failure APIResult instead of crashing.
        # data={} = empty dict (no data to return on failure).
        # success=False = signals to the caller that this failed.
        # error=str(e) = convert exception to readable string for logging/display.
        return APIResult(source=source, data={}, success=False, error=str(e))


# fetch_all fetches ALL APIs simultaneously and returns all results.
# This is the main function — it orchestrates all the concurrent fetching.
# -> list[APIResult] = returns one APIResult per API, all in a list.
async def fetch_all() -> list[APIResult]:

    # Define the list of APIs to fetch.
    # Each tuple = (url, source_label).
    # These are free public APIs — no API key needed.
    apis = [
        # Bitcoin price from CoinDesk API.
        ("https://api.coindesk.com/v1/bpi/currentprice.json", "bitcoin"),
        # Random advice from AdviceSlip API.
        ("https://api.adviceslip.com/advice", "advice"),
        # Name-based age prediction API.
        ("https://api.agify.io/?name=ahmed", "agify"),
    ]

    # Create ONE shared aiohttp session for all requests.
    # "async with" = async context manager — automatically closes session when done.
    # ONE session for ALL requests is efficient:
    #   - Reuses TCP connections (connection pooling).
    #   - Creating a new session per request is wasteful and slow.
    async with aiohttp.ClientSession() as session:

        # List comprehension: create a coroutine for each API — but DON'T await yet.
        # fetch_one(session, url, name) returns a coroutine object (not a result).
        # We collect all coroutines first, then run them all at once below.
        # If we awaited here: await fetch_one(...) — that would be SEQUENTIAL (slow).
        # We want PARALLEL, so we collect first, gather second.
        coroutines = [fetch_one(session, url, name) for url, name in apis]

        # asyncio.gather(*coroutines) runs ALL coroutines simultaneously.
        # * unpacks the list: gather(coro1, coro2, coro3) — takes individual args.
        # await = wait here until ALL coroutines finish.
        # Results come back in THE SAME ORDER as the input coroutines.
        # If bitcoin is index 0, results[0] = bitcoin result — always.
        results = await asyncio.gather(*coroutines)

    # Convert tuple (returned by gather) to list — easier to work with.
    # gather returns a tuple of results, one per coroutine.
    return list(results)
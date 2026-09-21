# asyncio = needed for asyncio.run() — starts the async event loop.
import asyncio

# time = for measuring sync execution time in run_sync().
import time

# urllib.request = built-in sync HTTP library.
# We use this (not aiohttp) in run_sync() to show the BLOCKING behavior.
# It's intentionally slow — that's the point of the comparison.
import urllib.request

# json = parse the response body from urllib (it returns bytes, not dict).
import json

# fetch_all = our async fetcher that gets all 3 APIs simultaneously.
from fetcher import fetch_all

# async_timer = our timing decorator to measure async function duration.
from timer import async_timer


# @async_timer = applies our timing decorator to run_async.
# This automatically prints how long run_async() takes when called.
# We don't need to manually add timing code inside the function.
@async_timer
# run_async fetches all 3 APIs in parallel and prints the results.
# -> None = returns nothing, just prints output.
async def run_async() -> None:

    # fetch_all() runs all 3 API calls simultaneously.
    # await = pause here until all 3 are done (but they run in parallel).
    # results = list of APIResult objects, one per API.
    results = await fetch_all()

    # Print header for the async results section.
    print("\n📦 Async Results:")

    # Loop through each result and print it.
    for r in results:

        # Check if this particular API call succeeded.
        if r.success:

            # r.data is a dict — list(r.data.keys()) gives all top-level keys.
            # [:3] = show only the first 3 keys — avoid printing massive dicts.
            # This tells us the structure of the response without drowning in data.
            print(f"  ✅ {r.source}: keys={list(r.data.keys())[:3]}")
        else:

            # Print which API failed and why.
            # r.error = the exception message from fetch_one's except block.
            print(f"  ❌ {r.source}: {r.error}")


# run_sync fetches 2 APIs sequentially (one after another) — the old, slow way.
# We use it ONLY to show the contrast with async.
# -> None = returns nothing, just prints timing.
def run_sync() -> None:

    # Only 2 URLs here (not 3) to keep the comparison fair-ish.
    # Even 2 sync requests will be slower than 3 async ones.
    urls = [
        ("https://api.adviceslip.com/advice", "advice"),
        ("https://api.agify.io/?name=ahmed", "agify"),
    ]

    # Record start time before any requests.
    start = time.perf_counter()

    # Loop through each URL — this is SEQUENTIAL, not parallel.
    # The second request CANNOT start until the first one finishes.
    # Python sits and waits (blocking) for each response.
    for url, name in urls:

        # urllib.request.urlopen = synchronous (blocking) HTTP call.
        # "with" context manager = auto-closes the response when done.
        # This BLOCKS the entire program until the response arrives.
        with urllib.request.urlopen(url) as resp:

            # resp.read() = download the response body as bytes.
            # json.loads() = parse bytes as JSON → Python dict.
            # We don't use the result — just proving it completes successfully.
            json.loads(resp.read())

    # Calculate and print total time for both sequential requests.
    elapsed = time.perf_counter() - start
    print(f"🐢 Sync version (2 requests): {elapsed:.2f}s")


# Standard Python entry point.
# Only runs when this file is executed directly (python main.py).
# Not when it's imported by another module.
if __name__ == "__main__":

    # Print header for the async section.
    print("=== ASYNC VERSION (3 requests simultaneously) ===")

    # asyncio.run() = start the event loop and run run_async() inside it.
    # This is the ONLY correct way to call async code from sync code at top level.
    # run_async is decorated with @async_timer — timing prints automatically.
    asyncio.run(run_async())

    # Print separator before sync section.
    print("\n=== SYNC VERSION (2 requests sequentially) ===")

    # run_sync is a plain function — no asyncio needed, just call it directly.
    run_sync()

    # Final message summarizing the lesson.
    print("\n💡 Async fetched 3 APIs faster than sync fetched 2.")
    print("   This difference grows with more API calls (AI backends call many LLMs).")
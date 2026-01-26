import httpx
import psutil
import asyncio
import gc
import os
import urllib.parse
from pympler import tracker, refbrowser

def get_rss():
    p = psutil.Process()
    mem_info = p.memory_info()
    vms = mem_info.vms
    rss = mem_info.rss
    return rss / 1024.0

def output_function(o):
    return F"{type(o)} ({id(o)})"

async def _main() -> None:
    gc.collect()
    memory_tracker = tracker.SummaryTracker()
    memory_tracker.print_diff()
    for i in range(10):
        async with httpx.AsyncClient() as client:
            await client.request("HEAD", "http://www.google.com/")

            # cb = refbrowser.ConsoleBrowser(client, maxdepth=3, str_func=output_function)
            # cb.print_tree()
        await client.aclose()
        del client

        await asyncio.sleep(0.1)
        #gc.collect()
        rss = get_rss()
        print(f"Loop #{i}: {rss:,} kB")
    memory_tracker.print_diff()


if __name__ == "__main__":
    asyncio.run(_main())

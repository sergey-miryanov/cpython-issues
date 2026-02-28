import asyncio
import contextlib

work_done = False

async def cursor():
    try:
        yield 1
    finally:
        assert work_done

async def rows():
    global work_done
    try:
        yield 2
    finally:
        await asyncio.sleep(0.1) # <--- This line causes the issue
        work_done = True


async def main():
    async with contextlib.aclosing(cursor()) as ccursor:
        async for c in ccursor:
            async with contextlib.aclosing(rows()) as crows:
                async for r in crows:
                    break
                break

asyncio.run(main())

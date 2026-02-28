from contextvars import ContextVar
import contextlib
import asyncio

ctx = ContextVar('ctx', default=0)

async def agen():
    try:
        yield 1
    finally:
        ctx.set(1)

async def main():
    # async with contextlib.aclosing(agen()) as cgen:
    cgen = agen()
    if True:
        async for i in cgen:
            print(ctx.get())
            break
    await asyncio.sleep(1)
    await cgen.aclose()
    print(ctx.get())
asyncio.run(main())

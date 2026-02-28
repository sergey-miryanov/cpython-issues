import contextlib

async def gen():
    try:
        yield 1
    finally:
        print('finalize inner')

async def func():
    try:
        # async with contextlib.aclosing(gen()) as g:
        g = gen()
        if True:
            async for x in g:
                break
    finally:
        print('finalize outer')

import asyncio
asyncio.run(func())
print('END')

# import asyncio

# async def coro_a():
#    print("a")

# async def coro_b():
#    print("b")

# async def main():
#     task_b = asyncio.create_task(coro_b())
#     print('c')
#     await asyncio.sleep(1)
#     print('d')
#     await asyncio.create_task(coro_a())
#     await task_b

# asyncio.run(main())

import asyncio


async def consumer():
    for idx in range(100):
        await asyncio.sleep(0)
        message = yield idx
        print('received', message)


async def amain():
    agenerator = consumer()
    await agenerator.asend(None)

    fa = asyncio.create_task(agenerator.asend('A'))
    fb = asyncio.create_task(agenerator.asend('B'))
    await fa
    await fb

asyncio.run(amain())

import asyncio

async def agenfn():
    try:
        yield 10
    finally:
        await asyncio.sleep(0)

async def main():
    agen = agenfn()
    print(await anext(agen))
    del agen

asyncio.run(main())

from controller.pipeline import run_pipeline

async def main():
    data = await run_pipeline()
    return data

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(main())
    print(result)
[200~import asyncio

async def my_task():
    try:
        print("Task started")
        # Simulate some asynchronous work
        await asyncio.sleep(5)
        print("Task completed")
    except asyncio.CancelledError:
        print("Task was cancelled")

async def main():
    # Start the task
    task = asyncio.create_task(my_task())

    # Wait for some time before cancelling the task
    await asyncio.sleep(2)

    # Cancel the task
    task.cancel()

    try:
        # Wait for the task to be cancelled
        await task
    except asyncio.CancelledError:
        pass

    print("Execution continues")

# Run the main coroutine
asyncio.run(main())


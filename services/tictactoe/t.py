import asyncio

# async def my_task():
#     try:
#         print("Task started")
#         # Simulate some asynchronous work
#         await asyncio.sleep(5)
#         print("Task completed")
#     except asyncio.CancelledError:
#         print("Task was cancelled")

# async def main():
#     # Start the task
#     task = asyncio.create_task(my_task())

#     # Wait for some time before cancelling the task
#     await asyncio.sleep(2)

#     # Cancel the task
#     task.cancel()

#     try:
#         # Wait for the task to be cancelled
#         await task
#     except asyncio.CancelledError:
#         pass

#     print("Execution continues")

# # Run the main coroutine
# asyncio.run(main())
async def f1():
    print("hello1")
    print("hello2")
    # for i in range(1000000):
    #     print(1)
    await asyncio.sleep(3)
    print("hello3")

async def f2():
    print("1hello1")
    print("1hello2")

async def f3():
    for i in range(1000000):
        print(2)
    print("kaka")
    return

async def one():
    t2 = asyncio.create_task(f1())
    t1 = asyncio.create_task(f2())
    await f3()
    await t2
    await t1

asyncio.run(one())
# asyncio.create_task(f1)
# task = f1()
# # await task
# f2()
    
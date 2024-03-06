# import asyncio

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

arr = {}

class test:
    def __init__( self, id ):
        self.__id = id
        print("construct")
    
    def fun( self ):
        print(self.__id in arr) 
        arr.pop( self.__id )
        print("remove elem")
        print(self.__id in arr)

    def __del__( self ):
        print("destructor")

arr["yoy"] = test("yoy")

arr["yoy"].fun()

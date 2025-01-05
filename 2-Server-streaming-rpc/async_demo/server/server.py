from grpclib.server import Server
from rpc.streaming_grpc import GreeterBase
from rpc.streaming_pb2 import GreetingResponse

class GreeterService(GreeterBase):
    async def StreamGreetings(self, stream):
        request = await stream.recv_message()
        for i in range(5):  # Giả lập gửi 5 phản hồi
            response = GreetingResponse(message=f"Hello {request.name}, message {i+1}")
            await stream.send_message(response)

async def main():
    server = Server([GreeterService()])
    await server.start(host='127.0.0.1', port=50051)
    print("Server started at 127.0.0.1:50051")
    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        print("Server shutting down...")
        await server.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

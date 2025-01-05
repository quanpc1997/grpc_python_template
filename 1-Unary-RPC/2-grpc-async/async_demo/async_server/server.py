from grpclib.server import Server
from rpc.greeter_pb2 import HelloRequest, HelloReply
from rpc.greeter_grpc import GreeterBase

class GreeterService(GreeterBase):
    async def SayHello(self, stream):
        request = await stream.recv_message()
        reply = HelloReply(message=f"Hello, {request.name}!")
        await stream.send_message(reply)

async def main():
    server = Server([GreeterService()])
    await server.start(host="127.0.0.1", port=50051)
    print("Server is running on 127.0.0.1:50051")
    await server.wait_closed()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

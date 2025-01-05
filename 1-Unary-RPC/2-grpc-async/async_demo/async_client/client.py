from grpclib.client import Channel
from rpc.greeter_pb2 import HelloRequest
from rpc.greeter_grpc import GreeterStub

async def main():
    channel = Channel(host="127.0.0.1", port=50051)
    stub = GreeterStub(channel)

    response = await stub.SayHello(HelloRequest(name="Alice"))
    print(response.message)

    channel.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

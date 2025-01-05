import asyncio
from grpclib.client import Channel
from rpc.streaming_grpc import GreeterStub
from rpc.streaming_pb2 import GreetingRequest

async def main():
    channel = Channel(host='127.0.0.1', port=50051)
    stub = GreeterStub(channel)

    # Tạo request
    request = GreetingRequest(name="Alice")
    
    # Gọi hàm và await để lấy stream
    stream = await stub.StreamGreetings(request)
    
    for response in stream:
        print("Received:", response.message)

    channel.close()

if __name__ == "__main__":
    asyncio.run(main())

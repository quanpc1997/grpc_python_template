# Triển khai gRPC trong Python

## I. Triển khai đồng bộ
Các gói thư viện cần sử dụng
```sh
pip install grpcio grpcio-tools
```
```grpcio```: Là 1 thư viện Python. Cung cấp các API để tạo client và server gRPC, giúp bạn gửi và nhận các cuộc gọi RPC.
```grpcio-tools```: Thư viện của google chủ yếu hỗ trợ đồng bộ
Tại cả Server A(Client) và B đều phải khai báo file sau:
```protobuf
syntax = "proto3";

package unary;

service Unary{
  // A simple RPC.
  //
  // Obtains the MessageResponse at a given position.
 rpc GetServerResponse(Message) returns (MessageResponse) {}

}

message Message{
 string message = 1;
}

message MessageResponse{
 string message = 1;
 bool received = 2;
}
```

Ở đay ta khai báo 1 Service(class) với 1 method là GetServerResponse:
- Truyền vào là 1 đối tượng Message với thuộc tính là message. 
- Trả về 1 đối tượng MessageResponse với 2 thuộc tính là message và received.

Sau đó ta chạy lệnh sau:
```sh
python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.
```
Lệnh này sẽ sinh ra stub với 2 file:
- **unary_pb2.py**: Chứa các định nghĩa về Request và Response.
- **unary_pb2_grpc.py**: Chứa các lớp để kết nối server và client, bao gồm: định nghĩa service, định nghĩa stub, phương thức đăng ký server với gRPC.

### 1. Server:

Định nghĩa lại service bằng cách kế thừa từ **filename_pb2_grpc.Servicer** và các method liên quan.
```python
class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        # get the string from the incoming request
        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'message': result, 'received': True}

        return pb2.MessageResponse(**result)
```

Sau đó tạo server gRPC
```python
def serve():
    # tạo ra một server có thể xử lý nhiều yêu cầu gRPC đồng thời với tối đa 10 worker threads.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Thêm servicer vào server gRPC
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    # Cấu hình cổng của server
    server.add_insecure_port('[::]:50051')
    # Chạy server gRPC
    server.start()
    # giúp server chạy liên tục không bị thoát.
    server.wait_for_termination()
```

### 2. Client
Tạo instance:
```python
# Tạo một channel giữa client server.
self.channel = grpc.insecure_channel("localhost:50051")
# Tạo liên kết giữa 2 stub
self.stub = pb2_grpc.UnaryStub(self.channel)
# Tạo Message
message = pb2.Message(message=message)
# Gọi hàm Remote
self.stub.GetServerResponse(message)
```

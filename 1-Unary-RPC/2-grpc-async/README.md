# II. Triển khai bất đồng bộ
Cài đặt các thư viện cần thiết:
```sh
pip install grpcio grpclib grpcio-tool grpc-interceptor
```
```grpcio```: Là 1 thư viện Python. Cung cấp các API để tạo client và server gRPC, giúp bạn gửi và nhận các cuộc gọi RPC.
```grpclib```: Thư viện của python hỗ trợ bất đồng bộ(trái ngược với grpcio-tool)
```grpcio-tools```: Thư viện của google chủ yếu hỗ trợ đồng bộ
Tại cả Server A(Client) và B đều phải khai báo file sau:

Chú ý câu lệnh gen ra file python grpc:
```python
python -m grpc_tools.protoc -I. --python_out=. --grpclib_python_out=. greeter.proto
```

Câu lệnh này sử dụng thêm tham số grpclib_python_out để gen ra file bất đồng bộ
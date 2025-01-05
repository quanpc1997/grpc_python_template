# gRPC - Google Remote Producer Call

## I. gRPC
### 1. Tại sao gọi là Remote Producer Call?

Remote Procedure Call có nghĩa là: **gọi một hàm ở một máy từ xa (remote machine) như thể hàm đó nằm trong chương trình của bạn**. Server A sẽ gọi 1 hàm ở server B thông qua 1 stub được định nghĩa ở cả server A và B thông qua file ```.proto```. Khi A gọi thì sẽ gọi hàm (giả) trong stub và stub sẽ có vai trò serialize và gửi dữ liệu qua mạng bằng HTTP/2, server sẽ chạy hàm tương tự đó.

> Chú ý: GRPC chỉ sử dụng để Server nói chuyện với Server khác.

### 2. Stub là gì?
Stub trong gRPC là một lớp hoặc đối tượng được tự động sinh ra từ tệp .proto, đóng vai trò trung gian giúp client giao tiếp với server. Stub trừu tượng hóa quá trình:

- Đóng gói dữ liệu (serialize) từ định dạng ứng dụng thành protobuf.
- Gửi request qua HTTP/2 đến server.
- Nhận response từ server, giải mã (deserialize) và trả kết quả về ứng dụng client.
Về bản chất, stub giúp client "giống như" đang gọi một hàm cục bộ, nhưng thực chất là một Remote Procedure Call (RPC) đến server.

### 3. Kiến trúc gRPC
![gRPC Architecture](/images/1-grpc-architecture.png)

Khi User gửi request đến API(người dùng không thể tương tác trực tiếp với gRPC) ở Server A. API sẽ gọi hàm trong stub với  parameter(nếu có). Stub sẽ chuyển nó về dạng nhị phân rồi gửi đến cho Server B(sử dụng protobuf). Server B nhận packages và gọi đến stub của mình, decode và nhận yêu cầu. Sau khi thực hiện xong thì gửi lại response đã được xử lý cho Protobuf xử lý. Server A nhận được packet thì cũng decode rồi trả kết quả cho API. API trả kết quả cho user dưới dạng json/xml.   

### 4. Sự khác biệt giữa gRPC và REST
gRPC hoạt động tương tự REST trong việc gửi request và nhận response. Tuy nhiên, gRPC khác REST ở nhiều khía cạnh quan trọng:

- **Serialization (Định dạng dữ liệu)**
gRPC: Dữ liệu được mã hóa bằng Protocol Buffers (protobuf), là định dạng nhị phân, giúp giảm kích thước dữ liệu và tăng tốc độ truyền tải.
REST: Dữ liệu thường ở định dạng JSON hoặc XML (văn bản), lớn hơn và chậm hơn để phân tích cú pháp (parsing).
- **Giao thức truyền tải**
    - **gRPC**: Sử dụng HTTP/2, hỗ trợ các tính năng nâng cao như:
        - **Multiplexing**: Gửi nhiều request trên cùng một kết nối mà không phải chờ request trước hoàn thành.
        - **Header nén**: Giảm băng thông.
        - **Streaming**: Cho phép truyền dữ liệu theo luồng giữa client và server (client streaming, server streaming, bidirectional streaming).

    - **REST**: Sử dụng HTTP/1.1, không hỗ trợ multiplexing và streaming hiệu quả.
- **Kiểu gọi API**
    - **gRPC**: Hỗ trợ 4 kiểu gọi RPC:
        - **Unary RPC**: (1 request -> 1 response) giống REST.
        - **Server streaming RPC**: Server gửi nhiều phản hồi cho 1 request.
        - **Client streaming RPC**: Client gửi nhiều request, server trả về 1 response.
        - **Bidirectional streaming RPC**: Cả client và server truyền dữ liệu song song.

    - **REST**: Chủ yếu chỉ hỗ trợ 1 request -> 1 response.

- **Định nghĩa API**
    - **gRPC**: Sử dụng tệp .proto để định nghĩa API, message và kiểu dữ liệu. Tệp này được biên dịch thành mã nguồn (stub) cho client/server. Điều này đảm bảo cả hai bên có cùng giao thức và kiểu dữ liệu.
    - **REST**: Định nghĩa API thường thông qua tài liệu (Swagger/OpenAPI), nhưng không tự động đồng bộ mã nguồn giữa client và server.
- **Header và cấu trúc**
    - **gRPC**: Có cấu trúc đơn giản, không cần header phức tạp. Tất cả metadata (như authentication) có thể được truyền qua metadata gRPC.
    - **REST**: Sử dụng header HTTP, thường yêu cầu client và server phải quản lý các thông tin như Authorization, Content-Type, v.v.
- **Hiệu suất**
    - **gRPC**: Tối ưu hóa cho hiệu suất và độ trễ thấp, đặc biệt phù hợp với microservices hoặc các hệ thống yêu cầu thời gian thực.
    - **REST**: Chậm hơn do sử dụng JSON/XML và HTTP/1.1, nhưng dễ sử dụng và tương thích rộng hơn.

####  Ví dụ minh họa
**REST API (JSON)**
- Client gửi request:

```http
POST /api/say-hello HTTP/1.1
Host: example.com
Content-Type: application/json

{
    "name": "Alice"
}
```

- Server trả response:

```json
{
    "message": "Hello, Alice"
}
```

**gRPC (protobuf)**
- Client gọi stub:

```python
response = stub.SayHello(HelloRequest(name="Alice"))
print(response.message)
```
Dữ liệu được truyền dưới dạng nhị phân protobuf qua HTTP/2:

```protobuf
message HelloRequest {
    string name = 1;
}

message HelloResponse {
    string message = 1;
}
```
#### Khi nào nên dùng gRPC hay REST?
| Tiêu chí                 | gRPC                               | REST                                 |
|--------------------------|------------------------------------|-----------------------------------|
| Hiệu suất                | Cao (protobuf, HTTP/2)             | Trung bình (JSON/XML, HTTP/1.1)      |
| Truyền dữ liệu streaming | Rất tốt                            | Không hiệu quả                       |
| Hỗ trợ đa ngôn ngữ       | Mạnh (stub auto-gen từ .proto)     | Tùy thuộc vào công cụ và tài liệu    |
| Đơn giản và phổ biến     | Cần học thêm (protobuf, streaming) | Phổ biến, dễ sử dụng                 |
| Tích hợp với trình duyệt | Không trực tiếp                    | Dễ (HTTP và JSON/XML)                |


**Tóm lại:**
gRPC khác REST ở việc:

- Tối ưu hóa hiệu suất (nhờ protobuf và HTTP/2).
- Đơn giản hóa việc định nghĩa và đồng bộ client/server qua tệp .proto.
- Hỗ trợ các kiểu gọi nâng cao như streaming và bidirectional.

Tuy nhiên, nếu bạn cần giao tiếp với trình duyệt hoặc hệ thống không hỗ trợ protobuf/HTTP/2, REST vẫn là lựa chọn phù hợp.

## 5. Xem thêm
[1. Unary RPC](./1-Unary-RPC/README.md)
[2. Server streaming RPC](./2-Server-streaming-rpc/README.md)
[3. Client streaming RPC](./3-Client-streaming-rpc/README.md)
[4. Bidirectional streaming RPC](./4-Bidirectional-streaming-rpc/README.md)

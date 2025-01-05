import grpc
from concurrent import futures
import time
import rpc.unary_pb2_grpc as pb2_grpc
import rpc.unary_pb2 as pb2


class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        # get the string from the incoming request
        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'message': result, 'received': True}

        return pb2.MessageResponse(**result)


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


if __name__ == '__main__':
    serve()
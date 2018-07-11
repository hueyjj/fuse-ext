from concurrent import futures
import time

import grpc

import proto.youtube_pb2 as youtube_pb2
import proto.youtube_pb2_grpc as youtube_pb2_grpc

class Youtube(youtube_pb2_grpc.YoutubedlServiceServicer):
    
    def FindYoutubeMusic(self, request, context):
        return youtube_pb2.YtMusicReply(name=request.name, status=youtube_pb2.YtMusicReply.Status.EXIST)

def serve():
    print(youtube_pb2.YtMusicReply.EXIST)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    youtube_pb2_grpc.add_YoutubedlServiceServicer_to_server(Youtube(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
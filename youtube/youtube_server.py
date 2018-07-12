from concurrent import futures
import time

import grpc

import proto.youtube_pb2 as youtube_pb2
import proto.youtube_pb2_grpc as youtube_pb2_grpc

from youtube import download_music

class Youtube(youtube_pb2_grpc.YoutubeServiceServicer):
    
    def FindYoutubeMusic(self, request, context):
        print("Received youtube music find request: " + request.url)
        return youtube_pb2.YtMusicReply(name=request.url, status=youtube_pb2.YtMusicReply.MUSIC_EXIST)
    
    def DownloadYoutubeMusic(self, request, context):
        print("Received youtube music download request: " + request.url)
        ret_code = download_music(request.url)
        status = youtube_pb2.YtMusicReply.DOWNLOAD_SUCCESS
        if ret_code is not 0:
            status = youtube_pb2.YtMusicReply.DOWNLOAD_FAIL
        return youtube_pb2.YtMusicReply(name=request.url, status=status)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    youtube_pb2_grpc.add_YoutubeServiceServicer_to_server(Youtube(), server)
    server.add_insecure_port('[::]:9090')
    server.start()
    print("Server starting...")
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
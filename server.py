import asyncio
import logging
import json
import platform
import threading
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
from grpc.experimental import aio
from webrtc_pusher.autogen import webrtc_pusher_pb2_grpc as webrtc_pusher_pb2_grpc
from webrtc_pusher.autogen import webrtc_pusher_pb2 as webrtc_pusher_pb2_pb2
from webrtc_pusher.remote import start as communicate_with_signaling_server


class WebRTC_Pusher_Service(webrtc_pusher_pb2_grpc.WebRTC_PusherServicer):
    def __init__(self):
        self.pcs = set()

    async def Negotiate(self, request, context):
        message = request
        sdp = message.sdp
        type_ = message.type

        offer = RTCSessionDescription(sdp=sdp, type=type_)

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        options = {"framerate": "30", "video_size": "640x480"}
        player = MediaPlayer("/dev/video0", format="v4l2", options=options)

        await pc.setRemoteDescription(offer)
        for t in pc.getTransceivers():
            if t.kind == "audio" and player.audio:
                pc.addTrack(player.audio)
            elif t.kind == "video" and player.video:
                pc.addTrack(player.video)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        response = webrtc_pusher_pb2_pb2.SDP(sdp=pc.localDescription.sdp, type=pc.localDescription.type)
        return response


async def _start_async_server():
    server = aio.server()
    server.add_insecure_port("[::]:50051")
    webrtc_pusher_pb2_grpc.add_WebRTC_PusherServicer_to_server(
        WebRTC_Pusher_Service(), server
    )
    await server.start()
    await server.wait_for_termination()


def run_webrtc_service():
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    loop.create_task(_start_async_server())
    loop.run_forever()


if __name__ == '__main__':
    t = threading.Thread(target=communicate_with_signaling_server, args=["http://dji-asdk-to-python.herokuapp.com"])
    t.start()
    run_webrtc_service()

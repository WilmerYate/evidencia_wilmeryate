import grpc
from webrtc_pusher.autogen import webrtc_pusher_pb2 as webrtc_pusher_pb2
from webrtc_pusher.autogen import webrtc_pusher_pb2_grpc as webrtc_pusher_pb2_grpc

def negotiate(ip_server, sdp, type_):
    sdp = webrtc_pusher_pb2.SDP(sdp=sdp, type=type_)
    channel = grpc.insecure_channel(ip_server)
    stub = webrtc_pusher_pb2_grpc.WebRTC_PusherStub(channel)
    response = stub.Negotiate(sdp)
    return {"sdp": response.sdp, "type": response.type}

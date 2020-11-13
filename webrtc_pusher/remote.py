import socketio, asyncio, concurrent.futures
from webrtc_pusher.negotiate import negotiate

def start(signalig_server):
    sio = socketio.Client()

    @sio.event
    def connect():
        sio.emit("create_room", "secret_key_pusher")

    @sio.event
    def viewer_need_offer(data):
        viewer_id = data["viewer_id"]
        remote_description = data["offer"]
        print("Server ask for offer to viewer " + viewer_id)
        answer = negotiate("localhost:50051", remote_description["sdp"], remote_description["type"])
        sio.emit("offer_to_viewer", {"viewer_id": viewer_id, "offer": answer})

    @sio.event
    def disconnect():
        print('Disconnected from server')

    sio.connect(signalig_server)
    sio.wait()

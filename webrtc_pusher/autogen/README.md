# Generate pb2.py and pb2_grpc.py files from protos

```bash
python -m grpc_tools.protoc -I . --python_out=webrtc_pusher/autogen --grpc_python_out=webrtc_pusher/autogen --proto_path=protos webrtc_pusher.proto
```

# Fix imports on *_pb2_grpc.py files, example:

```python
import webrtc_pusher_pb2 as webrtc_pusher__pb2
# to
from webrtc_pusher.autogen import webrtc_pusher_pb2 as webrtc_pusher__pb2
```

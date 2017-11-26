import re
import socket
import threading

from FFmpegVideoCapture import FFmpegVideoCapture
from VideoStream import VideoStream


class XiaoYiActionCamera:
    STREAM_URL = 'rtsp://%s:554/live'

    DEFAULT_IP_ADDRESS = '192.168.42.1'
    DEFAULT_PORT = 7878

    DEFAULT_STREAM_WIDTH = 640
    DEFAULT_STREAM_HEIGHT = 480

    def __init__(
            self,
            ip_address=DEFAULT_IP_ADDRESS,
            stream_width=DEFAULT_STREAM_WIDTH,
            stream_height=DEFAULT_STREAM_HEIGHT
    ):
        self.ip_address = ip_address
        self.stream_width = stream_width
        self.stream_height = stream_height

    def open_stream(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.ip_address, XiaoYiActionCamera.DEFAULT_PORT))

        server.send(b'{"msg_id":257,"token":0}')

        data = str(server.recv(512))
        while "rval" not in data:
            data = str(server.recv(512))
        token = re.findall('"param": (.+) }', data)[0]

        stop_stream = bytes('{"msg_id":260,"token":%s}' % token, encoding='ascii')
        server.send(stop_stream)

        start_stream = bytes('{"msg_id":259,"token":%s,"param":"none_force"}' % token, encoding='ascii')
        server.send(start_stream)

        def drain_camera_socket():
            ignored = server.recv(512)
            while ignored:
                ignored = server.recv(512)

        drain = threading.Thread(target=drain_camera_socket, args=())
        drain.setDaemon(True)
        drain.start()

        return VideoStream(FFmpegVideoCapture(
            XiaoYiActionCamera.STREAM_URL % self.ip_address,
            self.stream_width,
            self.stream_height,
            'bgr24'
        ))

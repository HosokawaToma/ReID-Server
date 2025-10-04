from webrtc_recorder import RTCIceServer, RTCConfiguration

class ApplicationRtcConfiguration:
    def __init__(self, server_ip: str, turn_username: str, turn_password: str):
        self.server_ip = server_ip
        self.turn_username = turn_username
        self.turn_password = turn_password

    def get_configuration(self):
        return RTCConfiguration(
            iceServers=[
                RTCIceServer(
                    urls=[
                        f"stun:{self.server_ip}:3478",
                        f"turn:{self.server_ip}:3478",
                    ],
                    username=self.turn_username,
                    credential=self.turn_password,
                )
            ]
        )

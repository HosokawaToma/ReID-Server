from aiortc import RTCIceServer, RTCConfiguration

class ApplicationRtcOfferConfiguration:
    def __init__(self, host: str, port: str, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_configuration(self):
        return RTCConfiguration(
            iceServers=[
                RTCIceServer(
                    urls=[
                        f"stun:{self.host}:{self.port}",
                        f"turn:{self.host}:{self.port}",
                    ],
                    username=self.username,
                    credential=self.password,
                )
            ]
        )

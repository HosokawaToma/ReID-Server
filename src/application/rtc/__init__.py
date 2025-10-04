from application.rtc.peer_connection import ApplicationRtcPeerConnection
from application.rtc.configuration import ApplicationRtcConfiguration


class ApplicationRtc:
    def __init__(self, server_ip: str, turn_username: str, turn_password: str):
        self.server_ip = server_ip
        self.turn_username = turn_username
        self.turn_password = turn_password
        self.peer_connections: list[ApplicationRtcPeerConnection] = []
        self.configuration = ApplicationRtcConfiguration(
            self.server_ip, self.turn_username, self.turn_password)

    async def offer(self, client_id: int, sdp: str, sdp_type: str):
        peer_connection = ApplicationRtcPeerConnection(client_id, self.configuration)
        self.peer_connections.append(peer_connection)
        return await peer_connection.offer(sdp, sdp_type)

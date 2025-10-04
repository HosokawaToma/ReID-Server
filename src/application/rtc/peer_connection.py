import asyncio
from webrtc_recorder import RTCPeerConnection, MediaRecorder, RTCSessionDescription
from application.rtc.configuration import ApplicationRtcConfiguration

class ApplicationRtcPeerConnection:
    def __init__(self, client_id: int, configuration: ApplicationRtcConfiguration):
        self.client_id = client_id
        self.configuration = configuration.get_configuration()
        self.peer_connection = RTCPeerConnection(configuration=self.configuration)
        self.peer_connection.on("connectionstatechange", self._on_connectionstatechange)
        self.peer_connection.on("track", self._on_track)

    async def _on_connectionstatechange(self):
        if self.peer_connection.connectionState == "failed":
            await self.close()

    async def _on_track(self, track):
        if track.kind == "video":
            self.recorder = MediaRecorder(f"results/rtc/{self.client_id}.mp4")
            self.recorder.addTrack(track)
            await self.recorder.start()
        asyncio.create_task(self.consume_frames(track))

    async def consume_frames(self, track):
        try:
            while True:
                await track.recv()
                self.frame_count += 1
        except Exception:
            pass

    async def close(self):
        if self.recorder:
            await self.recorder.stop()
            self.recorder = None
        await self.peer_connection.close()

    async def offer(self, sdp: str, sdp_type: str) -> dict:
        offer = RTCSessionDescription(sdp=sdp, type=sdp_type)
        await self.peer_connection.setRemoteDescription(offer)
        answer = await self.peer_connection.createAnswer()
        await self.peer_connection.setLocalDescription(answer)
        return {"sdp": self.peer_connection.localDescription.sdp, "type": self.peer_connection.localDescription.type}

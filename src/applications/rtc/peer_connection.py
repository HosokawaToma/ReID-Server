import os
from datetime import datetime
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRecorder
from aiortc.rtcrtpreceiver import RemoteStreamTrack
from aiortc import RTCConfiguration
from entities.jwt.camera_client import EntityJWTCameraClient
from entities.storage import EntityStorage
from entities.rtc.sdp import EntityRtcSdp


class ApplicationRtcPeerConnection:
    PATH_OF_RECORDING = "{path}/rtc/{camera_id}/{view_id}/{timestamp}.mp4"
    CONNECTION_STATE_CHANGE = "connectionstatechange"
    TRACK = "track"
    FAILED = "failed"
    CLOSED = "closed"

    def __init__(
        self,
        jwt_camera_client: EntityJWTCameraClient,
        offer_sdp: EntityRtcSdp,
        configuration: RTCConfiguration,
        storage: EntityStorage,
    ) -> None:
        self.peer_connection = RTCPeerConnection(configuration)
        self.session = RTCSessionDescription(
            sdp=offer_sdp.sdp, type=offer_sdp.type)
        filepath = self.PATH_OF_RECORDING.format(
            path=storage.path,
            camera_id=jwt_camera_client.camera_id,
            view_id=jwt_camera_client.view_id,
            timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
        )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.recorder = MediaRecorder(filepath)
        self.peer_connection.on(
            self.CONNECTION_STATE_CHANGE,
            self._on_connectionstatechange,
        )
        self.peer_connection.on(
            self.TRACK,
            self._on_track,
        )
        self.recorder_started = False

    async def _on_connectionstatechange(self):
        if self.peer_connection.connectionState in [self.FAILED, self.CLOSED]:
            await self.close()

    async def _on_track(self, track: RemoteStreamTrack):
        self.recorder.addTrack(track)
        if not self.recorder_started:
            self.recorder_started = True
            await self.recorder.start()

    async def close(self):
        if self.recorder_started:
            await self.recorder.stop()
            self.recorder_started = False
        await self.peer_connection.close()

    async def offer(self) -> EntityRtcSdp:
        await self.peer_connection.setRemoteDescription(self.session)
        answer = await self.peer_connection.createAnswer()
        await self.peer_connection.setLocalDescription(answer)
        return EntityRtcSdp(sdp=answer.sdp, type=answer.type)

import fastapi

from application.identify_person.background_process import ApplicationIdentifyPersonBackgroundProcess
from entities.identify_person.image import EntityIdentifyPersonImage


class ApplicationIdentifyPerson:
    def __init__(self):
        self.background_process = ApplicationIdentifyPersonBackgroundProcess()

    async def identify_person(self, identify_person_image: EntityIdentifyPersonImage) -> None:
        await self.background_process.add_task(identify_person_image)

    async def startup(self):
        await self.background_process.start()

    async def shutdown(self):
        await self.background_process.stop()

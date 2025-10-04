import asyncio
from asyncio import Queue

from entities.identify_person.image import EntityIdentifyPersonImage
from application.identify_person.background_process.clip_reid import ApplicationIdentifyPersonBackgroundProcessClipReID
from application.identify_person.background_process.storage import ApplicationIdentifyPersonBackgroundProcessStorage
from application.identify_person.background_process.database import ApplicationIdentifyPersonBackgroundProcessDatabase

class ApplicationIdentifyPersonBackgroundProcess:
    def __init__(self):
        self.running = False
        self.queue: Queue = None
        self.tasks: list[asyncio.Task] = []
        self.clip_reid = ApplicationIdentifyPersonBackgroundProcessClipReID()
        self.storage = ApplicationIdentifyPersonBackgroundProcessStorage()

    async def start(self):
        self.running = True
        self.queue = Queue()
        task = asyncio.create_task(self.process_queue())
        self.tasks.append(task)

    async def stop(self):
        self.running = False
        for task in self.tasks:
            task.cancel()
        self.tasks = []

    async def add_task(self, identify_person_image: EntityIdentifyPersonImage):
        if self.queue is not None:
            await self.queue.put(identify_person_image)

    async def process_queue(self):
        while self.running:
            try:
                identify_person_image = await self.queue.get()
                await self.process(identify_person_image)
            except asyncio.CancelledError:
                break

    async def process(self, identify_person_image: EntityIdentifyPersonImage):
        try:
            database = ApplicationIdentifyPersonBackgroundProcessDatabase()
            client_id = identify_person_image.client_id
            camera_model = database.get_camera(client_id)
            if camera_model is None:
                raise Exception("Camera not found")
            camera_id = camera_model.camera_id
            view_id = camera_model.view_id
            image = identify_person_image.image
            person_id = self.clip_reid.identify(image, camera_id, view_id)
            identify_person_image.camera_id = camera_id
            identify_person_image.view_id = view_id
            identify_person_image.person_id = person_id
            identify_person_image.filepath = self.storage.save(identify_person_image)
            await database.insert_identify_person_image(identify_person_image)
        except Exception as e:
            print(f"process処理でエラーが発生: {e}")

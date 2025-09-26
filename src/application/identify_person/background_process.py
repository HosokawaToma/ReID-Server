import asyncio
from asyncio import Queue

from entities.person_crop_image import EntityPersonCropImage
from service.database.person_crop_images import ServiceDatabasePersonCropImages
from service.identify_person import ServiceIdentifyPerson
from service.storage.person_crop_images import ServiceStoragePersonCropImages


class ApplicationIdentifyPersonBackgroundProcess:
    running = False
    queue: Queue = None
    tasks: list[asyncio.Task] = []

    @staticmethod
    async def start():
        ApplicationIdentifyPersonBackgroundProcess.running = True
        ApplicationIdentifyPersonBackgroundProcess.queue = Queue()
        task = asyncio.create_task(
            ApplicationIdentifyPersonBackgroundProcess.process_queue())
        ApplicationIdentifyPersonBackgroundProcess.tasks.append(task)
        print("バックグラウンド処理を開始しました")

    @staticmethod
    async def stop():
        ApplicationIdentifyPersonBackgroundProcess.running = False
        for task in ApplicationIdentifyPersonBackgroundProcess.tasks:
            task.cancel()
        ApplicationIdentifyPersonBackgroundProcess.tasks = []
        print("バックグラウンド処理を停止しました")

    @staticmethod
    async def add_task(person_crop_image: EntityPersonCropImage):
        if ApplicationIdentifyPersonBackgroundProcess.queue is not None:
            await ApplicationIdentifyPersonBackgroundProcess.queue.put(person_crop_image)
            print(f"タスクをキューに追加しました: {person_crop_image.id}")

    @staticmethod
    async def process_queue():
        print("process_queue開始")
        while ApplicationIdentifyPersonBackgroundProcess.running:
            try:
                # 非同期でキューから取得
                person_crop_image = await ApplicationIdentifyPersonBackgroundProcess.queue.get()
                print(f"タスクを処理開始: {person_crop_image.id}")
                await ApplicationIdentifyPersonBackgroundProcess.process(person_crop_image)
                print(f"タスク処理完了: {person_crop_image.id}")
            except asyncio.CancelledError:
                print("process_queueがキャンセルされました")
                break
            except Exception as e:
                print(f"process_queueでエラーが発生: {e}")

    @staticmethod
    async def process(person_crop_image: EntityPersonCropImage):
        try:
            image = person_crop_image.image
            camera_id = person_crop_image.camera_id
            view_id = person_crop_image.view_id
            service_identify_person = ServiceIdentifyPerson()
            person_id = service_identify_person.Identify(
                image, camera_id, view_id)
            person_crop_image.person_id = person_id
            person_crop_image.filepath = ServiceStoragePersonCropImages.save(
                person_crop_image)
            ServiceDatabasePersonCropImages.insert(person_crop_image)
        except Exception as e:
            print(f"process処理でエラーが発生: {e}")

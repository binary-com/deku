from services import Services
from client import Client
import docker
import logging
import asyncio
import re

class Trigger(Client):
    def __init__(self, client):
        self.client = client
        self.services = Services(client)

    def get_latest_images(self, image_url):
        images = self.client.images.pull(image_url)
        return images

    async def check_for_update(self, service_filter=None):
        service_list = self.services.get(service_filter)

        for service in service_list:
            image = service.attrs.get('Spec')['TaskTemplate']['ContainerSpec']['Image']
            imageFormat = re.match('([^:@]*):([^@:]*)', image)
            print(imageFormat.groups())
            [name, tag] = imageFormat.groups()
            #images = await self.get_latest_images(name)
            #print(images)

triggerObject = Trigger(docker.from_env())
loop = asyncio.get_event_loop()
loop.run_until_complete(triggerObject.check_for_update())


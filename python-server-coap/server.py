#!/usr/bin/env python3

import struct
import asyncio

import aiocoap.resource as resource
import aiocoap

from aiocoap.numbers.codes import Code


class LedResource(resource.Resource):
    """Control led status"""

    def __init__(self):
        super().__init__()
        self.led = False

    async def render_get(self, request):
        request = request
        response = b'on\0' if self.led else b'off\0'
        return aiocoap.Message(payload=response)

    async def render_put(self, request):
        print(f'PUT payload {request.payload}')
        self.led = not self.led
        return aiocoap.Message(code=Code.CHANGED)


class TemperatureResource(resource.Resource):
    """Temperature publish endpoint"""

    def __init__(self):
        super().__init__()
        self.temperature = -1.0

    async def render_get(self, request):
        request = request
        response = struct.pack('f', self.temperature)
        return aiocoap.Message(payload=response)

    async def render_put(self, request):
        self.temperature = struct.unpack('f', request.payload)[0]
        print(f"PUT temperature: {self.temperature}")
        return aiocoap.Message(code=Code.CHANGED)


def main():
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
                      resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['led'], LedResource())
    root.add_resource(['temperature'], TemperatureResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()

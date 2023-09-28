import asyncio
import sys

from viam.services.vision import VisionClient
from viam.module.module import Module
from .facialdetector import FacialDetector

async def main():
    module = Module.from_args()
    module.add_model_from_registry(VisionClient.SUBTYPE, FacialDetector.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())

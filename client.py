import asyncio
import os
from PIL import Image

from viam import logging
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient
from viam.rpc.dial import Credentials, DialOptions

# these must be set, you can get them from your robot's 'CODE SAMPLE' tab
robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    creds = Credentials(type="robot-location-secret", payload=robot_secret)
    opts = RobotClient.Options(refresh_interval=0, dial_options=DialOptions(credentials=creds), log_level=logging.DEBUG)
    return await RobotClient.at_address(robot_address, opts)


async def main():
    robot = await connect()

    print("Resources:")
    print(robot.resource_names)

    fd = VisionClient.from_robot(robot, name="face-detector")

    im = Image.open(r"./test/father_son.jpg") 
    print(im)
    detections = await fd.get_detections_from_camera("cam")
    print(detections)
    
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
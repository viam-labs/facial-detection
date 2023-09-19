from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image
from deepface import DeepFace

from viam.media.video import RawImage
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.utils import ValueTypes

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.service.vision import Detection
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.vision import Vision

from viam.components.camera import Camera

from viam.logging import getLogger

import time
import asyncio
import numpy

LOGGER = getLogger(__name__)

class FacialDetector(Vision, Reconfigurable):
    
    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "detector"), "facial-detector")
    # opencv, retinaface, mtcnn, ssd, dlib, mediapipe or yolov8
    detection_framework: str

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        frameworks = ['opencv', 'retinaface', 'mtcnn', 'ssd', 'dlib', 'mediapipe','yolov8']
        detection_framework = config.attributes.fields["detection_framework"].string_value or 'ssd'
        if not detection_framework in frameworks:
            raise Exception("detection_framework must be one of 'opencv', 'retinaface', 'mtcnn', 'ssd', 'dlib', 'mediapipe','yolov8'")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.detection_framework = config.attributes.fields["detection_framework"].string_value or 'ssd'
        return
    
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        cam = Camera.from_robot(self.parent, camera_name)
        cam_image = await cam.get_image()
        return self.get_detections(cam_image)
    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        # note that some of the detector frameworks do not like RGBA, so we convert to RGB
        results = DeepFace.extract_faces(img_path=numpy.array(image.convert('RGB')),enforce_detection=False, detector_backend=self.detection_framework)
        detections = []
        for r in results:
            if r["confidence"] > 0:
                detections.append({ "confidence": r["confidence"], "class_name": "face", "x_min": r["facial_area"]["x"], "y_min": r["facial_area"]["y"], 
                                    "x_max": r["facial_area"]["x"] + r["facial_area"]["w"], "y_max": r["facial_area"]["y"] + r["facial_area"]["h"]} )
        return detections

    async def do_command(self):
        return
    
    async def get_classifications(self):
        return
    
    async def get_classifications_from_camera(self):
        return
    
    async def get_object_point_clouds(self):
        return
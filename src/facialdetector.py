from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from os import walk

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
    model_name: str
    verify_threshold: float
    disable_detect: bool
    disable_verify: bool
    path: str
    face_labels = {}
    
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
        models =  ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
        if not model_name in models:
            raise Exception("detection_framework must be one of 'VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.DEPS = dependencies
        self.detection_framework = config.attributes.fields["detection_framework"].string_value or 'ssd'
        self.model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
        self.verify_threshold = config.attributes.fields["verify_threshold"].number_value or .8
        self.disable_detect = config.attributes.fields["disable_detect"].bool_value
        self.disable_verify = config.attributes.fields["disable_verify"].bool_value

        # List all files and filter for jpgs, then load the jpgs into memory, assuming there are not that many
        self.path = config.attributes.fields["path"].string_value
        filenames = next(walk(self.path), (None, None, []))[2]
        for filename in filenames:
            if filename.endswith(".jpg"):
                name = filename.removesuffix(".jpg")
                image = Image.open(self.path+filename)
                self.face_labels[name] = image

        return
        
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, actual_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_detections(cam_image)
    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        detections = []
        if self.disable_detect == False:
            results = DeepFace.extract_faces(img_path=numpy.array(image.convert('RGB')),enforce_detection=False, detector_backend=self.detection_framework)
            for r in results:
                if r["confidence"] > 0:
                    detection = { "confidence": r["confidence"], "class_name": "face", "x_min": r["facial_area"]["x"], "y_min": r["facial_area"]["y"], 
                                        "x_max": r["facial_area"]["x"] + r["facial_area"]["w"], "y_max": r["facial_area"]["y"] + r["facial_area"]["h"]}
                    if self.disable_verify == False:
                        v = await self.verify_image(image)
                        if len(v) and v["confidence"] >= self.verify_threshold:
                            detection = v
                    detections.append(detection)            
        elif self.disable_verify == False:
            v = await self.verify_image(image)
            if len(v):
                detections.append(v)
        
        return detections

    async def verify_image(self, image: Union[Image.Image, RawImage]):
        detection = {}
        for label in self.face_labels:
                r = DeepFace.verify(distance_metric="euclidean_l2", enforce_detection=False, align=False, model_name=self.model_name, detector_backend=self.detection_framework, img1_path = numpy.array(self.face_labels[label].convert('RGB')), img2_path = numpy.array(image.convert('RGB')))
                if r["verified"] == True:
                    detection = { "confidence": r["distance"]/r["threshold"], "class_name": label, "x_min": r["facial_areas"]["img2"]["x"], "y_min": r["facial_areas"]["img2"]["y"], 
                                        "x_max": r["facial_areas"]["img2"]["x"] + r["facial_areas"]["img2"]["w"], "y_max": r["facial_areas"]["img2"]["y"] + r["facial_areas"]["img2"]["h"]}
                    break;
        return detection
    
    async def do_command(self):
        return
    
    async def get_classifications(self):
        return
    
    async def get_classifications_from_camera(self):
        return
    
    async def get_object_point_clouds(self):
        return
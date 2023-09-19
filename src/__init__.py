"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import VisionClient
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .facialdetector import FacialDetector

Registry.register_resource_creator(VisionClient.SUBTYPE, FacialDetector.MODEL, ResourceCreatorRegistration(FacialDetector.new, FacialDetector.validate))

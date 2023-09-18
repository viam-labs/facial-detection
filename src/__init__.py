"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import Vision
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .facialdetector import facialdetector

Registry.register_resource_creator(Vision.SUBTYPE, facialdetector.MODEL, ResourceCreatorRegistration(facialdetector.new, facialdetector.validate))

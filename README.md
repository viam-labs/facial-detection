# facial-detector modular service

*facial-detector* is a Viam modular vision service that uses the [DeepFace](https://github.com/serengil/deepface) library to perform facial detections

## API

The facial-detector resource provides the following methods from Viam's built-in [rdk:service:vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html)

### get_detections(image=*binary*)

### get_detections_from_camera(camera_name=*string*)

## Viam Service Configuration

The following attributes may be configured as speech service config attributes.
For example: the following configuration would set up listening mode, use an ElevenLabs voice "Antoni", make AI completions available, and use a 'Gollum' persona for AI completions:

``` json
{
  "detection_framework": "ssd"
}
```

### detection_framework

*enum - "opencv"|"retinaface"|"mtcnn"|"ssd"|"dlib"|"mediapipe"|"yolov8"|"google" (default: "ssd")*

The detection framework to use for facial detection.  `ssd` is chosen as the default for a good balance of speed and accuracy.

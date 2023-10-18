# facial-detector modular service

*facial-detector* is a Viam modular vision service that uses the [DeepFace](https://github.com/serengil/deepface) library to perform facial detections

## Prerequisites

``` bash
sudo apt update && sudo apt upgrade -y
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
```

## API

The facial-detector resource provides the following methods from Viam's built-in [rdk:service:vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html)

### get_detections(image=*binary*)

Note: any detected face will return with the label "face", unless labels are specified via [face_labels](#face_labels).

### get_detections_from_camera(camera_name=*string*)

Note: any detected face will return with the label "face", unless labels are specified via [face_labels](#face_labels).

## Viam Service Configuration

The following attributes may be configured as facial-detector config attributes.
For example: the following configuration would use the `ssd` framework:

``` json
{
  "detection_framework": "ssd"
}
```

Note: if you are going to use *get_detections_from_camera()*, you will need to set any camera that you plan to use as a dependency for this service.

### detection_framework

*enum - "opencv"|"retinaface"|"mtcnn"|"ssd"|"dlib"|"mediapipe"|"yolov8" (default: "ssd")*

The detection framework to use for facial detection.  `ssd` is chosen as the default for a good balance of speed and accuracy.

### face_labels

*object*

If configured, expects an object map of key:label, value:path to use in matching against reference face images.
For example:

``` json
{
  "matt": "/path/to/matt.jpg",
  "suzy": "/path/to/suzy_photo.jpg"
}
```

If the input image from get_detections() or get_detections_from_camera() verifies as a match of one of the images specified in the *face_labels* paths, the associated label will be returned.

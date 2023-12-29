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

### get_detections_from_camera(camera_name=*string*)

Note: if using this method, any cameras you are using must be set in the `depends_on` array for the service configuration, for example:

```json
      "depends_on": [
        "cam"
      ]
```

## Viam Service Configuration

The following attributes may be configured as facial-detector config attributes.
For example: the following configuration would use the `ssd` framework:

``` json
{
  "detection_framework": "ssd"
}
```

### detection_framework

*enum - "opencv"|"retinaface"|"mtcnn"|"ssd"|"dlib"|"mediapipe"|"yolov8" (default: "ssd")*

The detection framework to use for facial detection.  `ssd` is chosen as the default for a good balance of speed and accuracy.

### recognition_model

*enum -   "VGG-Face"|"Facenet"|"Facenet512"|"OpenFace"|"DeepFace"|"DeepID"|"ArcFace"|"Dlib"|"SFace" (default: "ArcFace")*

The model to use for facial recognition.  `ArcFace` is chosen as the default for a good balance of speed and accuracy.

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

### verify_threshold

*number(default:.8)*

If [disable_verify](#disable_verify) is false and [face_labels](#face_labels) are set, if the verification confidence does not match or exceed this threshold, it will return as a normal detected "face".

### disable_detect

*boolean(default:false)*

If [disable_verify](#disable_verify) is false and [face_labels](#face_labels) are set, if disable_detect is false, any faces detected but not verified as matching a label will be labeled as *face*.

### disable_verify

*boolean(default:false)*

If false and [face_labels](#face_labels) are set, will attempt to verify any faces detected.
If you only want verified faces to be labeled, set this to false and [disable_detect](#disable_detect) to true.

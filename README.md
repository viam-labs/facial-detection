# Facial Detector modular resource

This module implements the [vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html) in the `facial-detector` model and leverages the [DeepFace](https://github.com/serengil/deepface) library to perform facial detections.

## Requirements

This module is compatible with the following platforms:

- MacOS (darwin)
- Linux

Run the following command to get your operating system name, and then proceed to the instructions corresponding to your operating system.

```bash
uname -s
```

On MacOS:

`run.sh` will automatically install the following system dependencies if not already set up on the machine:

- `viam-sdk  >= 0.5.1`
- `deepface`
- `numpy`
- `pillow`
- `tensorflow==2.14.0rc1`
- `ml_dtypes==0.2.0`

On Linux:

``` bash
sudo apt update && sudo apt upgrade -y
sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y
```

## Configure your facial detector

> [!NOTE]
> Before configuring your facial-detector, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com/).
Click on the **Services** subtab and click **Create service**.
Select the `vision` type, then select the `detector:facial-detector` model. 
Click **Add module**, then enter a name for your facial detector and click **Create**.

On the new component panel, copy and paste the following attribute template into your vision service's **Attributes** box:

```json 
{
  "detection_framework": "<detection-framework>",
  "recognition_model": "<recognition-model>",
  "face_labels": {
    "matt": "<path-to-image-1>",
    "suzy": "<path-to-image-2>"
  },
  "verify_threshold": <verify-threshold>,
  "disable_detect": <disable-detect>,
  "disable_verify": <disable-verify>
}
```

> [!NOTE]
> For more information, see [Configure a Machine](https://docs.viam.com/manage/configuration/).

### Attributes 

The following attributes are available for `vision:facial-detector:ssd` facial-detectors:

| Name   | Type | Inclusion | Description| Supported |
|--------|-------|----------|------------|-----------|
| `detection_framework` | enum | Optional| The detection framework to use for facial detection.<br> Default: `ssd`, for a good balance of speed and accuracy. | `"opencv"`, `"retinaface"`, `"mtcnn"`, `"ssd"`, `"dlib"`, `"mediapipe"`, `"yolov8"` |
| `recognition_model` | enum | Optional| The model to use for facial recognition.<br> Default: `ArcFace`, for a good balance of speed and accuracy.| `"VGG-Face"`, `"Facenet"`, `"Facenet512"`, `"OpenFace"`, `"DeepFace"`, `"DeepID"`, `"ArcFace"`, `"Dlib"`, `"SFace"` |                     |
| `face_labels` | object  | Optional | An object map of `key:label, value:path` for matching against reference face images. | - |
| `verify_threshold` | number  | Optional | If `disable_verify` is set to `false` and `face_labels` are set, this threshold must be met or exceeded for a verification match.<br> Default: `0.8` | - |
| `disable_detect` | bool | Optional| If set to `false`, any faces detected but not verified as matching a label will be labeled as "face".<br> Default: `false` | - |
| `disable_verify` | bool | Optional | If set to `false` and `face_labels` are set, will attempt to verify any faces detected. If you only want verified faces, set `disable_verify` and `disable_detect` to `true`.<br> Default: `false` | - |


### Example configuration 

```json
{
  "detection_framework": "ssd",
  "recognition_model": "ArcFace",
  "face_labels": {
    "matt": "/path/to/matt.jpg",
    "suzy": "/path/to/suzy_photo.jpg"
  },
  "verify_threshold": 0.8,
  "disable_detect": false,
  "disable_verify": false
}
```

## API

The `facial-detector` resource provides the following methods from [Viam's vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html):

| Method   | Parameters | Description |
|--------|-------|----------|
| [`get_detections`](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections) | `image` | Get a list of detections in the given image using the specified detector.|
 | [`get_detections_from_camera`](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications_from_camera) | `camera_name=string` | Get a list of classifications in the next image given a camera and a classifier.|

### Next Steps

- To test your vision service, go to the [Control tab](https://docs.viam.com/fleet/machines/#control).
- To write code against your vision service, use one of the [available SDKs](https://docs.viam.com/program/).
- Check out the [Create a Facial Verification System](https://docs.viam.com/tutorials/projects/verification-system/#configure-a-verification-system) tutorial that uses this module.

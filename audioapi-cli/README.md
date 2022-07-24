<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; audioapi-cli Package</h1>
A simple CLI which is used to give the client an easy and fast access to InSoundz AudioAPI.
<br />
<br />

## Installation
- Please make sure you are running python3.7 or later.
```console
pip install audioapi-cli
```

## Help
| Command       | Description   | 
| ------------- |:-------------|
| enhance-file | Sends an audio file (by URL or local path) to InSoundz AudioAPI and receives an enhanced audio file |

### Command: enhance-file 

| Argument                          | Description   | Required | Default |
| -------------------------------- |:-------------|:-------------:|:-------------|
| api-token       | Authentication key to access InSoundz AudioAPI services | Yes | None |
| endpoint-url    | Use an alternative endpoint URL (without the 'http://' prefix) | No | api.insoundz.io |
| src             | A URL or a local path of the original audio file | Yes | None |
| no-download     | If set, the enhanced file won't be downloaded to the local machine (we'll get only the URL of the enhanced file) | No | False|
| dst             | A URL to upload the enhanced file or a local path to download the enhanced file | No | <current_path>/<original_filename>_enhanced.<original_suffix> |
| retention | URL Retention duration [minutes] | No | None |
| status-interval | Check the audio enhancement process every <status-interval> [seconds] | No | 1 second|

## Getting started
```console
audioapi_cli <command> <arg1> <arg2> ...
```

### Example #1:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "<current_path>/example_enhanced.wav").
```console
audioapi_cli enhance-file --api-token="my-key" --src="/home/example_user/my_audio_files/example.wav"
```

### Example #2:
Send a URL of an audio file and at the end of the audio enhancement process download the enhanced file to our local machine (to "/home/example_user/my_enhanced_files_dir/new_file.wav").
```console
audioapi_cli enhance-file --api-token="my-key" --src="https://api.insoundz.io/examples/example_file.wav" --dst="/home/example_user/my_enhanced_files_dir/new_file.wav
```

### Example #3:
Upload an audio file from our local machine and at the end of the audio enhancement process don't download the enhanced files and request to keep the URL of the enhanced file valid for 8 hours.
```console
audioapi_cli enhance-file --api-token="my-key" --src="/home/example_user/my_audio_files/example.wav" --no-download --retention=480
```
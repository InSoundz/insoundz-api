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
| Command       | Description                  |
|---------------|:-----------------------------|
| config        | Set or view config variables |
| enhance-file  | Enhance audio file           |
| version       | Display versions             |

### Command: config

| Sub-command | Description             |
|-------------|:------------------------|
| get         | Echo config variables   |
| set         | Update config variables |

### Sub-command: config get

| Argument | Description | Required | Default |
|--------- |:------------|:---------|:--------|
| None     | None        | None     | None    |

### Sub-command: config set

| Argument  | Description | Required | Default |
|-----------|:------------|:---------|:--------|
| client-id | Client ID for InSoundz AudioAPI services. If not set, the CLI uses the permently configured client ID. If set, the CLI will use this client ID only for this session | None | None |
| secret    | Secret key to access InSoundz AudioAPI services. If not set, the CLI uses the permently configured secret key. If set, the CLI will use this secret key only for this session | None | None |
| url       | Use an alternative endpoint URL (without the 'http://' prefix). If not set, the CLI uses the permently configured url. If set, the CLI will use this url only for this session. If not set and not permently configured, the CLI will use the default url | None | api.insoundz.io |

### Command: enhance-file 

| Argument        | Description | Required | Default |
|-----------------|:------------|:---------|:--------|
| client-id       | Client ID for InSoundz AudioAPI services. If not set, the CLI uses the permently configured client ID. If set, the CLI will use this client ID only for this session | If not set with config command | None |
| secret          | Secret key to access InSoundz AudioAPI services. If not set, the CLI uses the permently configured secret key. If set, the CLI will use this secret key only for this session | If not set with config command | None |
| url             | Use an alternative endpoint URL (without the 'http://' prefix). If not set, the CLI uses the permently configured url. If set, the CLI will use this url only for this session. If not set and not permently configured, the CLI will use the default url | None | api.insoundz.io |
| src             | A local path of the original audio file | Yes | None |
| no-download     | If set, the enhanced file won't be downloaded to the local machine (we'll get only the URL of the enhanced file) | No | False|
| dst             | A local path or file to download the enhanced file | No | <current_path>/<original_filename>_enhanced.<original_suffix> |
| retention       | URL Retention duration [minutes] | No | None |
| status-interval | Check the enhancement process every <status_interval> [seconds] | No | 0.5 |
| no-progress-bar | If set, progress-bar won't be displayed | No | False |

### Command: version 

| Argument | Description | Required | Default |
|----------|:------------|:---------|:--------|
| None     | None        | None     | None    |

## Getting started
```console
audioapi_cli <command> <arg1> <arg2> ...
```

### Example #1:
Get versions.
```console
audioapi_cli version
```

### Example #2:
Permently set client ID and secret key.
```console
audioapi_cli config set --client-id XXXX-XXXX-XXXX-XXXX --secret XXXX-XXXX-XXXX-XXXX
```

### Example #3:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "<current_path>/example_enhanced.wav").
```console
audioapi_cli enhance-file --api-token="my-key" --src="/home/example_user/my_audio_files/example.wav"
```

### Example #4:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "/home/example_user/my_enhanced_files_dir/new_file.wav").
```console
audioapi_cli enhance-file --api-token="my-key" --src="/home/example_user/my_audio_files/example.wav" --dst="/home/example_user/my_enhanced_files_dir/new_file.wav
```

### Example #5:
Upload an audio file from our local machine and at the end of the audio enhancement process don't download the enhanced files and request to keep the URL of the enhanced file valid for 8 hours.
```console
audioapi_cli enhance-file --api-token="my-key" --src="/home/example_user/my_audio_files/example.wav" --no-download --retention=480
```

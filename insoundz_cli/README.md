<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; insoundz-cli Package</h1>
A simple CLI which is used to give the client an easy and fast access to insoundz API.
<br />
<br />

![PyPI](https://img.shields.io/pypi/v/insoundz-cli)
![PyPI - License](https://img.shields.io/pypi/l/insoundz-cli)
![PyPI - OS](https://img.shields.io/badge/Operating%20System-OS%20Independent-green)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/insoundz-cli)

## Installation
To enable the auto-complete support, you will have to pip install from source and not from wheel.
```console
pip install --no-binary insoundz-cli insoundz-cli
```
Otherwise, you can just run:
```console
pip install insoundz-cli
```
NOTE: Please make sure you are running python3.7 or later.

## Help
| Command       | Description                   |
|---------------|:------------------------------|
| config        | Set or view config variables. |
| enhance-file  | Enhance audio file.           |

### Command: config

| Sub-command | Description              |
|-------------|:-------------------------|
| get         | Echo config variables.   |
| set         | Update config variables. |

### Sub-command: config get

| Argument | Description | Required | Default |
|--------- |:------------|:---------|:--------|
| None     | None        | None     | None    |

### Sub-command: config set

| Argument    | Description | Required | Default |
|-------------|:------------|:---------|:--------|
| --client-id | Client ID for insoundz API services. If not set, the CLI uses the permanently configured client ID. If set, the CLI will use this client ID only for this session. | None | None |
| --secret    | Secret key to access insoundz API services. If not set, the CLI uses the permanently configured secret key. If set, the CLI will use this secret key only for this session. | None | None |
| --url       | Use an alternative endpoint URL (without the 'http://' prefix). If not set, the CLI uses the permanently configured url. If set, the CLI will use this url only for this session. If not set and not permanently configured, the CLI will use the default url. | None | api.insoundz.io |

### Command: enhance-file 

| Argument        | Description | Required | Default |
|-----------------|:------------|:---------|:--------|
| --client-id       | Client ID for insoundz API services. If not set, the CLI uses the permanently configured client ID. If set, the CLI will use this client ID only for this session. | If not set with config command | None |
| --secret          | Secret key to access insoundz API services. If not set, the CLI uses the permanently configured secret key. If set, the CLI will use this secret key only for this session. | If not set with config command | None |
| --url             | Use an alternative endpoint URL (without the 'http://' prefix). If not set, the CLI uses the permanently configured url. If set, the CLI will use this url only for this session. If not set and not permanently configured, the CLI will use the default url. | No | api.insoundz.io |
| --src             | A local path of the original audio file. | Yes | None |
| --no-download     | If set, the enhanced file won't be downloaded to the local machine (we'll get only the URL of the enhanced file). | No | False|
| --dst             | A local path or file to download the enhanced file. | No | <current_path>/<original_filename>_enhanced.<original_suffix> |
| --retention       | URL Retention duration [minutes]. | No | None |
| --status-interval | Check the enhancement process every <status_interval> [seconds]. | No | 0.5 |
| --no-progress-bar | If set, progress-bar won't be displayed. | No | False |

## Getting started
```console
insoundz_cli <command> <arg1> <arg2> ...
```

### Example #1:
Permanently set client ID and secret key.
```console
insoundz_cli config set --client-id XXXX-XXXX-XXXX-XXXX --secret XXXX-XXXX-XXXX-XXXX
```

### Example #2:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "<current_path>/example_enhanced.wav").
```console
insoundz_cli enhance-file --src="/home/example_user/my_audio_files/example.wav"
```

### Example #3:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "/home/example_user/my_enhanced_files_dir/new_file.wav").
```console
insoundz_cli enhance-file --src="/home/example_user/my_audio_files/example.wav" --dst="/home/example_user/my_enhanced_files_dir/new_file.wav"
```

### Example #4:
Upload an audio file from our local machine and at the end of the audio enhancement process don't download the enhanced files and request to keep the URL of the enhanced file valid for 8 hours.
```console
insoundz_cli enhance-file --src="/home/example_user/my_audio_files/example.wav" --no-download --retention=480
```

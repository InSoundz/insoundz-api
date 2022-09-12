<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; insoundz-api Package</h1>
Insoundz API client implementation to produce audio enhancement.
<br />
<br />

![PyPI](https://img.shields.io/pypi/v/insoundz-api)
![PyPI - License](https://img.shields.io/pypi/l/insoundz-api)
![PyPI - OS](https://img.shields.io/badge/Operating%20System-OS%20Independent-green)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/insoundz-api)

## Installation
Please make sure you are running python3.7 or later.
```console
pip install insoundz-api
```

## Getting started: Audio file enhancement
Sending the original file for audio enhancement processing and download the enhanced file to our local machine.

```python
from insoundz_api.enhancer import AudioEnhancer

enhancer = AudioEnhancer(client_id="my_client_id", secret="my_secret")
enhancer.enhance_file(
    src="/home/example_user/my_audio_files/example.wav", 
    dst="/home/example_user/my_enhanced_files_dir"
)
```

```console
$ cd /home/example_user/my_enhanced_files_dir
$ ls
example_file_enhanced.wav
```

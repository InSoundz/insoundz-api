<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; audioapi Package</h1>
InSoundz audioapi client implementation to produce audio enhancement.
<br />
<br />

## Installation
- Please make sure you are running python3.7 or later.
```console
pip install audioapi
```

## Getting started: Audio file enhancement
Sending the original file for audio enhancement processing and download the enhanced file to our local machine.

```python
from audioapi.enhancer import AudioEnhancer

enhancer = AudioEnhancer(api_token="my_key")
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

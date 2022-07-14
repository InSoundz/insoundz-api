<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; audioapi-cli Package</h1>
A simple CLI which is used to give the client an easy and fast access to Insoundz AudioAPI.
<br />
<br />

## Installation
- Please make sure you are running python3.7 or later.
```console
pip install audioapi-cli
```

## Getting started

### Example #1:
Upload an audio file from our local machine and at the end of the audio enhancement process download the enhanced file to our local machine (to "<local_path>/example_enhanced.wav").
```console
audioapi_cli enhance-file --api-token="my-user-key" --url-endpoint="oaiw7rf0af.execute-api.us-east-1.amazonaws.com/debug" --src-type=local --src-path="/home/user/my_audio_files/example.wav"
```

### Example #2:
Send a URL of an audio file and at the end of the audio enhancement process download the enhanced file to our local machine (to "/home/user/my_enhanced_files/new_file.wav").
```console
audioapi_cli enhance-file --api-token="my-user-key" --url-endpoint="oaiw7rf0af.execute-api.us-east-1.amazonaws.com/debug" --src-type=remote --dst-path="/home/user/my_enhanced_files/new_file.wav" --src-path="https://insoundz-wavs.s3.us-east-1.amazonaws.com/audioapi_tmp/file_example_WAV_10MG.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAgaDGV1LWNlbnRyYWwtMSJGMEQCIFcuMRndSZu8FQWPPJUzZNt6VObjyHxfgyDO4v8UdoQDAiAS2pioJFiQmhUuZJms4nDRJ4nwVu71WIF1ntyupRnAMir7AghBEAEaDDkwNDIxODQ1ODU5OSIMY4JLL3KL2lZmEXZEKtgCetNtG6Y10NpSfJ%2FS4U3Lwq4EswaEVni1EZYGwihkbAPAk57eblZkstqFeaHLT4tvlj44mP7%2BSbEvbqgFCTuEPuj8XS0Zano54T6A3PpYke8MT%2F7rsZTWkiREOp%2BRUoHIy5MzyiyMp2FX0FTWSTcgAiPV9Wz70lVUZFlrIaLf545T8mnEJsJWEZEYXFkLZiBwD91pXFGMS28DI%2FtVA7%2BC4mwU6adTxPLZNuyas4W6D8mX7LLm%2Fvury9OeFfpWiNS9K91EWO%2FVyoMoKD85QeX9zlSsxsdNqZGs3GH2%2B5f3c6lFiMagGsD0%2B3hwUzb7AXC%2BQ7n9%2BThS9LFwzMpLJBKSk0N%2Bk%2BnqjEhAaUDJaRQe3uDQKAKrQvU32NcEd0LsHeNFOIHWHIutCqUGXzV0iKmh4%2BT1ub3fORmtvVMThup%2Bd5T7jm2hkh29RBFG1oMUISWUr69e7Ug87hgwu5GvlgY6tAIDXo%2By7qL%2FX5uuKemm3R91eC%2Bf9XqGGdGERnqEsP%2Fl6nM%2BQQlkHKARqsxsbK%2Bp3Sp1Zd1Eh5f4KhB2mjbJULgISrAx5TOPkKFTsNDERqxe5tRFuhFicxnBnLpPtmn%2BM4duPKaJMt92n%2Bl0XIpK9EnlArzSRHeTSiJmqNm%2Bc4Gq5EB%2FRianPrTSIJqbKfILh%2B1r3QXEc%2FHv9%2FU80dBP9LyrSjWG6S5UObUnrLRj41%2FeCTJ2WifRylbvCV6AtWC1JR0GwW%2B1ePevbVw%2B9u8mVtwP1HufoVtqxchd4OLaiHYg%2BI4ggJOjlYKI2RWjRF0tjBILp4vkNPmjYvcMaHtkW3o%2F%2FvrMPRWPS8LM90L5EYmdUjHSnRP%2BHOJ7jgrGs4AEO72zlEIxigoh8RFF447FTPtTbj1j%2Fw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220711T180441Z&X-Amz-SignedHeaders=host&X-Amz-Expires=720&X-Amz-Credential=ASIA5FB46XHTWK6J4Q3S%2F20220711%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=1e5a145192e2a6a9afe2cac8719ed2d6605778d54f9f39a075111cafe0a2ae67"
```

### Example #3:
Upload an audio file from our local machine and at the end of the audio enhancement process don't download the enhanced files and request to keep the URL of the enhanced file valid for 8 hours.
```console
audioapi_cli enhance-file --api-token="my-user-key" --url-endpoint="oaiw7rf0af.execute-api.us-east-1.amazonaws.com/debug" --src-type=local --src-path="/home/user/my_audio_files/example.wav" --no-download --retention=480
```

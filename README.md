
# Insoundz AudioAPI Library
The AudioAPI library includes the audioapi package and the audioapi-cli package.

## audioapi Package
A simple pythonic client to access Insoundz AudioAPI for audio enhancement.

## audioapi-cli Package
A simple CLI which is used to give the client an easy and fast access to Insoundz AudioAPI (based uppon the audioapi package).

## Installation
- Make sure you are running python3.7 or later. 
- Run the following: 
```console
pip install git+https://gitlab.com/InSoundz/audioapi-cli.git@feature/INZ-1961#subdirectory=audioapi-pkg  
pip install git+https://gitlab.com/InSoundz/audioapi-cli.git@feature/INZ-1961#subdirectory=audioapi-cli-pkg  
```

## AWS credentials
- Before you run the AudioAPI-CLI, you must have AWS credentials  
- [Create a new AWS user](https://inz.atlassian.net/wiki/spaces/DEV/pages/1888157707/Creating+a+new+user+in+AWS)  
- [Getting AWS keys and configure AWS-CLI](https://inz.atlassian.net/wiki/spaces/DEV/pages/1740210177/Get+Access+Key+and+Secret+Key+and+configure+AWS-CLI)

## Running the AudioAPI-CLI
```console
git clone git@gitlab.com:InSoundz/audioapi-cli.git -b feature/INZ-1961  
cd audioapi-cli  
./audioapi_cli enhance-file --help  
./audioapi_cli enhance-file --api-endpoint="oaiw7rf0af.execute-api.us-east-1.amazonaws.com/debug" --src-type=local --src-path="/home/joseph/insoundz/audioapi-cli/examples/file_example_WAV_10MG.wav"
```

## Simple example
```console
./audioapi_cli enhance-file --api-endpoint="oaiw7rf0af.execute-api.us-east-1.amazonaws.com/debug" --src-type=local --src-path="/home/user/my_audio_files/example.wav"
```
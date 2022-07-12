<h1><img align="center" height="90" src="https://drive.google.com/uc?export=view&id=1b1DHDNsl_XGjtU_AK1QR9q_lSo3iLQ4x"> &nbsp; audioapi Package</h1>
A simple pythonic client to access Insoundz AudioAPI for audio enhancement.
<br />
<br />

## Getting started: Audio file enhancement
Sending the URL of the original file for audio enhancement process and download the enhanced file.

```python
def enhance_file(src_url, dst_path):

    api = audioapi.AudioAPI(api_token)
    ret_val = api.enhance_file(src_url)
    session_id = ret_val["session_id"]

    # Check status
    while True:
        ret_val = api.enhance_status(session_id)
        status = ret_val["status"]
        print(f"Session ID [{session_id}] job status [{status}].")

        if status == "done":
            enhanced_file_url = ret_val["url"]
            print(f"Enhanced file URL is located at {enhanced_file_url}")
            break
        elif status == "failure":
            failure_reason = ret_val["msg"]
            print(f"Failure reason: {failure_reason}")
            break
        else:
            time.sleep(3)

    # Downloading enhanced file
    wget.download(enhanced_file_url, dst_path)
```

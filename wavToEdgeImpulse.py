# pip install librosa (numpy, scipy dependencies)
# pip install requests

import librosa, wave
import json
import hmac, hashlib
import requests

API_URL = "https://ingestion.edgeimpulse.com/api/"
API_KEY = ""
HMAC_KEY =""
DEVICE_NAME =""
DEVICE_TYPE = ""



def createCborContent(audio_samples, interval_ms=0.0625):
    # empty signature (all zeros). HS256 gives 32 byte signature, and we encode in hex, so we need 64 characters here
    empty_sig = ''.join(['0'] * 64)
    
    json_content = {
        "protected": {
            "ver": "v1",
            "alg": "HS256"
        },
        "signature": empty_sig,
        "payload": {
            "device_name": DEVICE_NAME,
            "device_type": DEVICE_TYPE,
            "interval_ms": interval_ms,
            "sensors": [
                { "name": "audio", "units": "wav" }
            ],
            "values": audio_samples
        }
    }
    
    # encode in CBOR
    cbor_content = json.dumps(json_content)

    # sign message
    signature = hmac.new(bytes(HMAC_KEY, 'utf-8'), msg = cbor_content.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()

    # set the signature again in the message, and encode again
    json_content['signature'] = signature
    cbor_content = json.dumps(json_content)

    print(API_KEY)
    return cbor_content


# import wav samples as array
def importWavFile(fn):
    librosa_audio, librosa_sample_rate = librosa.load(fn, sr=16000, mono=True)

    # retrieve samples width in bits
    sample_width = 0
    with wave.open(fn, 'rb') as w: 
        sample_width = w.getsampwidth() * 8

    if sample_width == 8: # 8 bits is unsigned
        audio_samples = librosa_audio * 2**sample_width
    else: # > 16 bits is signed
        audio_samples = librosa_audio * 2**(sample_width-1)

    return audio_samples.tolist()


def uploadFile(cbor_content, file_name, label, data_type = "training"):
    res = requests.post(url=API_URL + data_type + "/data",
                        data=cbor_content,
                        headers={
                            'Content-Type': 'application/json',
                            'x-file-name': file_name,
                            'x-label': label,
                            'x-api-key': API_KEY
                        })
    if (res.status_code == 200):
        print('Uploaded file to Edge Impulse', res.status_code, res.content)
    else:
        print('Failed to upload file to Edge Impulse', res.status_code, res.content)




# main program
with open('credentials.json') as c:    
    credentials = json.load(c)
API_KEY = credentials['api_key']
HMAC_KEY = credentials['hmac_key']
DEVICE_NAME = credentials['device_name']
DEVICE_TYPE = credentials['device_type']

audio_samples = importWavFile('noise.11eq99bn.wav')
cbor_content = createCborContent(audio_samples, interval_ms=0.0625)
uploadFile(cbor_content, "test02", "noise")
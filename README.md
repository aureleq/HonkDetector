# Honk Detector
The aim of this project is to be able to detect sounds made by a car horn using Edge Impulse embedded machine learning solution.

We are using the [UrbanSound8K](https://urbansounddataset.weebly.com/) dataset to train our neural network.

## Requirements

You will need to create an account on [EdgeImpulse](edgeimpulse.com) first. It is also recommended to follow their tutorial on [sound recognition](https://docs.edgeimpulse.com/docs/audio-classification) to start with.

The project is based on [ST Discovery kit IOT node](https://www.st.com/en/evaluation-tools/b-l475e-iot01a.html) but it should work with any other supported hardware.

## Setup

- Download the UrbanSound8K following [this link](https://zenodo.org/record/1203745) and unzip its content
- Rename file `credentials.json.template` to `credentials.json`
- Update the json file with your EdgeImpulse credentials (api key, hmac key, device name)
- Install python `librosa` and `requests` packages

## Uploading wav files to ingestion service

The script `wavToEdgeImpulse.py` imports wav files from UrbanSound8K dataset and convert files to mono/16kHz format. They are uploaded to EdgeImpulse ingestion service in both training and testing datasets.

Some important variables and functions in the script:
- TESTING_SPLIT: part of files to consider as testing dataset. By default set to 25% (75% for training set)
- getWaveFiles(LABEL, 600, 0.5): by default we import 600 seconds of data , from which 50% is consider foreground sound. 

The script may run for a couple of minutes as a few hundreds samples have to be converted and uploaded to the ingestion service. All samples will then appear in your Edge Impulse dashboard.

## TODO

- Import some reference background noise or additional UrbanSound8K labels to complete neural network training
- Add field results
- Adapt default firmware to continously monitor sound from ST IOT kit

## References

- J. Salamon, C. Jacoby and J. P. Bello, "[A Dataset and Taxonomy for Urban Sound Research](http://www.justinsalamon.com/uploads/4/3/9/4/4394963/salamon_urbansound_acmmm14.pdf)", 22nd ACM International Conference on Multimedia, Orlando USA, Nov. 2014.
- Gideon Mendels, [How to apply machine learning and deep learning methods to audio analysis](https://towardsdatascience.com/how-to-apply-machine-learning-and-deep-learning-methods-to-audio-analysis-615e286fcbbc)
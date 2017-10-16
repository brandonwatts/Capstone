import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from oauth2client.client import GoogleCredentials

'''speech_api.py contains all the operations carried out by Google Speech API'''

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

'''Set the Credentials'''
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "CMSC323-edf53f65e546.json")
credentials = GoogleCredentials.get_application_default()


def parse_speech(wav_file):
    '''
    Method to parse the speech out of a wav file
    :param wav_file: .wav file
    :return: response from Google Speech API
    '''
    client = speech.SpeechClient()                                  # Instantiate a new Speech Client
    file_name = os.path.join(os.path.dirname(__file__),wav_file)    # Grab the file path of the .wav file

    with io.open(file_name, 'rb') as audio_file:                    # Load the .wav file into memory
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(                               # Set the configuration for the Speech input
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)                      # Generate a response

    return response
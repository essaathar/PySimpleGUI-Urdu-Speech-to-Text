import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import threading
import time

flag = False
def recog_speech(audio_data):
    # Step 2: Initialize recognizer
    recognizer = sr.Recognizer()

    # Step 3: Convert the audio to text
    with sr.AudioFile(audio_data) as source:
        audio_content = recognizer.record(source)
        
        try:
            # Recognize the text using Google's free Web Speech API
            text = recognizer.recognize_google(audio_content, language="ur-PK")
            print("Transcription: ", text)
            global flag
            flag=True
            # with open('transcript.txt', 'w') as file:
            #     file.write(text)
        except sr.RequestError:
            print("API was unreachable or unresponsive.")
        except sr.UnknownValueError:
            print("Unable to recognize speech.")

def do_other():
    while not flag:
        print("doing other things..")
        time.sleep(1)
    print("FINISHED doing other things!")

# Step 1: Load the MP3 file and convert it to audio data
mp3_audio = AudioSegment.from_mp3("audios/test.mp3")
audio_data = BytesIO()
mp3_audio.export(audio_data, format="wav")
audio_data.seek(0)

# Create and start the speech recognition thread
speech_thread = threading.Thread(target=recog_speech, args=(audio_data,))
speech_thread.start()

# Start the task thread
task_thread = threading.Thread(target=do_other)
task_thread.start()

# Wait for both threads to finish (optional)
speech_thread.join()
task_thread.join()
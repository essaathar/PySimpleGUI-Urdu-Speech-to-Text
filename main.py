import PySimpleGUI as sg
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import threading

# [sg.Text("اپ لوڈ کرنے کے لیے ایک MP3 فائل منتخب کریں", font=("Jameel Noori Nastaleeq", 12))],

layout = [
    [sg.Text("Select an MP3 file to upload:")],
    [sg.Input(), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),))],
    [sg.Button("Convert")],
    [sg.ProgressBar(10, key='-PROGRESS_BAR-', visible=False, size=(20,20))],
    [sg.Multiline(size=(60, 10), key='-OUTPUT-', font=("Jameel Noori Nastaleeq", 12))]
]

window = sg.Window("Urdu Speech-To-Text Converter!", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Convert":
        file_path = values[0]
        if file_path:
            
            try:
                # Step 1: Load the MP3 file and convert it to audio data
                mp3_audio = AudioSegment.from_mp3(file_path)
                audio_data = BytesIO()
                mp3_audio.export(audio_data, format="wav")
                audio_data.seek(0)

                # Step 2: Initialize recognizer
                recognizer = sr.Recognizer()

                # Step 3: Convert the audio to text
                with sr.AudioFile(audio_data) as source:
                    audio_content = recognizer.record(source)
                    window['-PROGRESS_BAR-'].update(visible=True)
                    window.refresh()
                    try:
                        # window['-PROGRESS_BAR-'].update(visible=True)
                        # window.refresh()
                        for i in range(1, 10):
                            window['-PROGRESS_BAR-'].update(current_count=i+1)
                            # time.sleep(1)
                            window.refresh()

                        # Recognize the text using Google's free Web Speech API
                        text = None                           
                        text = recognizer.recognize_google(audio_content, language="ur-PK")
                        while text is None:
                            print("transcribing...")
                        window['-OUTPUT-'].update(f"Transcription:\n{text}") 
                        # with open('transcript.txt', 'w') as file:
                        #     file.write(text)
                    except sr.RequestError:
                        window['-OUTPUT-'].update("API was unreachable or unresponsive.")
                    except sr.UnknownValueError:
                        window['-OUTPUT-'].update("Unable to recognize speech.")
            except Exception as e:
                window['-OUTPUT-'].update(f"Error: {e}")
        else:
            sg.popup("No file selected!")

window.close()

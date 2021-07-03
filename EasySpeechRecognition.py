from vosk import KaldiRecognizer
from vosk import Model
from vosk import SetLogLevel
import pyaudio
import pyttsx3

SetLogLevel(-1)

f = open('vocabulary.txt', 'r')
vocab = f.read().split(" ")
f.close()

i = 0
wordlist = []
while i < len(vocab)-1:
    towrite = '"' + vocab[i] + '"'
    wordlist.append(towrite)
    i += 1
words = str(wordlist).replace("'", "")

print(words)

MODEL = Model("model")
rec = KaldiRecognizer(MODEL, 16000, words)

P = pyaudio.PyAudio()
stream = P.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                frames_per_buffer=8000)
stream.start_stream()


def vocablisten():
    while True:
        DATA = stream.read(500, exception_on_overflow=False)
        if len(DATA) == 0:
            pass
        try:
            if rec.AcceptWaveform(DATA):
                string = rec.Result().rsplit(":")[-1][2:-3]
                if string != "":
                    print(string)
                    return string
        except Exception:
            print("No input")


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.say(text)
    # engine.save_to_file(text, 'lastcommand.wav')
    engine.runAndWait()


def listen():
    rec = KaldiRecognizer(MODEL, 16000)
    while True:
        # audioio.speak("ready")
        DATA = stream.read(5000, exception_on_overflow=False)
        if len(DATA) == 0:
            pass
        try:
            if rec.AcceptWaveform(DATA):
                string = rec.Result().rsplit(":")[-1][2:-3]
                if string != "":
                    print(string)
                    return string
        except Exception:
            pass

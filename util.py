import random
import os
import openai
from dotenv import load_dotenv
import pyttsx3
import os
import threading

def normalize(list):
    mag = sum(list)
    return [v / mag for v in list]

def make_cum(list):
    acc = 0
    for i in range(len(list)):
        temp = list[i]
        list[i] = acc
        acc += temp
    return list

class WeightedRandomMap:
    def __init__(self, list):
        self.names = [obj["name"] for obj in list]
        self.P = make_cum(normalize([obj["probability"] for obj in list]))
        assert len(self.names) == len(self.P)
    def get_rand(self):
        val = random.random()
        for i, p in enumerate(self.P):
            if p > val:
                return self.names[i - 1]
        return self.names[-1] 

def openai_query(message):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(model="text-davinci-003", prompt=message, temperature=.9, max_tokens=15)
    return response

def speak(message, callback):
    engine = pyttsx3.init()
    engine.setProperty("pitch", 300)
    engine.say(message)
    def f():
        engine.runAndWait()
        callback()
    threading.Thread(target=f).start()
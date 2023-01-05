import pyautogui
import random
import tkinter as tk
import json
import requests
import time

offline = True
# If not offline, it expects a HTTP URL
JSON_URL = "assets\\cc.json"
IMPATH = "assets\\"

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
            

class PetState:
    def __init__(self, json_obj):
        self.name = json_obj['state_name']
        self.frames = [tk.PhotoImage(file=IMPATH + json_obj['file_name'], format=f'gif -index {i}') for i in range(json_obj['frames'])]
        self.ox, self.oy, self.w, self.h = json_obj['dims']
        if 'move' in json_obj:
            self.dx, self.dy = json_obj['move']
        else:
            self.dx, self.dy = 0, 0
        self.next_states = WeightedRandomMap(json_obj['transitions_to'])
        

class Pet:
    def __init__(self, states):
        self.states = states
        self.current_state = list(states.values())[0]
        self.__current_frame = 0
        self.x, self.y = 200, 983

    def next_frame(self):
        output = self.current_state.frames[self.__current_frame]
        self.__current_frame += 1
        if self.__current_frame == len(self.current_state.frames):
            self.__state_change()
        self.x, self.y = (self.x + self.current_state.dx), (self.y + self.current_state.dy)
        return output

    def __state_change(self):
        self.set_state(self.current_state.next_states.get_rand())
    
    def set_state(self, name):
        self.current_state = self.states[name]
        self.__current_frame = 0

window = tk.Tk()

with open(JSON_URL) as config:
    config_obj = json.load(config)
    states = {state['state_name']: PetState(state) for state in config_obj}

pet = Pet(states)

def update():
    frame = pet.next_frame()
    label.configure(image=frame)
    window.geometry(f'{pet.current_state.w}x{pet.current_state.h}+{pet.x + pet.current_state.ox}+{pet.y + pet.current_state.oy}')
    window.after(100, update)

# window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
label.pack()

def handle_click(event):
    pet.set_state("miner_mutating")

window.bind("<Button-1>", handle_click)

window.after(1, update)
window.mainloop()

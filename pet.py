from util import WeightedRandomMap, openai_query, speak
from tkinter import simpledialog
import tkinter as tk
from os.path import join

def read_frames(impath):
        output = []
        i = 0
        while True:
            try:
                new_frame = tk.PhotoImage(file=join(impath),format=f'gif -index {i}')
                output.append(new_frame)
            except:
                break
            i += 1
        return output

class PetState:
    def __init__(self, json_obj, impath):
        self.name = json_obj['state_name']
        self.frames = read_frames(join(impath, json_obj['file_name']))
        self.ox, self.oy, self.w, self.h = json_obj['dims']
        if 'move' in json_obj:
            self.dx, self.dy = json_obj['move']
        else:
            self.dx, self.dy = 0, 0
        self.next_states = WeightedRandomMap(json_obj['transitions_to'])


class Pet:
    def __init__(self, states, window):
        self.states = states
        self.window = window
        self.current_state = list(states.values())[0]
        self.__current_frame = 0
        self.x, self.y = 45, 800

    def next_frame(self):
        output = self.current_state.frames[self.__current_frame]
        self.__current_frame += 1
        if self.__current_frame == len(self.current_state.frames):
            self.__state_change()
        self.x, self.y = (
            self.x + self.current_state.dx), (self.y + self.current_state.dy)
        return output

    def __state_change(self):
        self.set_state(self.current_state.next_states.get_rand())

    def set_state(self, name: str):
        self.current_state = self.states[name]
        self.__current_frame = 0
    
    def start_chat(self, prompt: str, listen_state: str, response_state: str, end_state: str):
        self.set_state(listen_state)
        query = simpledialog.askstring("ChatGPT Input", "What do you want to ask Bonzi?", parent=self.window)
        response = openai_query(prompt % query)
        self.set_state(response_state)
        speak(response, lambda: self.set_state(end_state))
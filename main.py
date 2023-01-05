from util import WeightedRandomMap, openai_query, speak
import tkinter as tk
from tkinter import simpledialog
import json

JSON_URL = "assets\\bonzi\\bonzi.json"
IMPATH = "assets\\bonzi\\"


class PetState:
    def __init__(self, json_obj):
        self.name = json_obj['state_name']
        self.frames = [tk.PhotoImage(file=IMPATH + json_obj['file_name'],
                                     format=f'gif -index {i}') for i in range(json_obj['frames'])]
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
        self.x, self.y = 100, 800

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

    def set_state(self, name):
        self.current_state = self.states[name]
        self.__current_frame = 0
    
    def start_chat(self, prompt: str, listen_state: str, response_state: str, end_state: str):
        self.set_state(listen_state)
        query = simpledialog.askstring("Input", "What do you want to ask Bonzi?")
        print(prompt % query)
        response = openai_query(prompt % query)
        self.set_state(response_state)
        speak(response["choices"][0]["text"], lambda: self.set_state(end_state))



def create_event_func(event, pet):
    if event["type"] == "state_change":
        return lambda e: pet.set_state(event["new_state"])
    elif event["type"] == "chatgpt":
        return lambda e: pet.start_chat(event["prompt"], event["listen_state"], event["response_state"], event["end_state"])


window = tk.Tk()

with open(JSON_URL) as config:
    config_obj = json.load(config)
    states = {state['state_name']: PetState(
        state) for state in config_obj["states"]}
    # Validate
    for state in states.values():
        for state in state.next_states.names:
            assert state in states

    pet = Pet(states)

    for event in config_obj["events"]:
        event_func = create_event_func(event, pet)
        if event["trigger"] == "click":
            window.bind("<Button-1>", event_func)


def update():
    frame = pet.next_frame()
    label.configure(image=frame)
    window.geometry(
        f'{pet.current_state.w}x{pet.current_state.h}+{pet.x + pet.current_state.ox}+{pet.y + pet.current_state.oy}')
    window.after(100, update)


# window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
label.pack()

window.after(1, update)
window.mainloop()

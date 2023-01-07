import tkinter as tk
import json
from pet import Pet, PetState
from os.path import join
import sys

if len(sys.argv) >= 1:
    CONFIG_PATH = sys.argv[0]
else:
    CONFIG_PATH = "assets\\bonzi\\"

def create_event_func(event, pet):
    if event["type"] == "state_change":
        return lambda e: pet.set_state(event["new_state"])
    elif event["type"] == "chatgpt":
        return lambda e: pet.start_chat(event["prompt"], event["listen_state"], event["response_state"], event["end_state"])


def update():
    frame = pet.next_frame()
    label.configure(image=frame)
    window.geometry(
        f'{pet.current_state.w}x{pet.current_state.h}+{pet.x + pet.current_state.ox}+{pet.y + pet.current_state.oy}')
    window.after(100, update)


if __name__ == "__main__":
    window = tk.Tk()

    with open(join(CONFIG_PATH, "config.json")) as config:
        config_obj = json.load(config)
        states = {state['state_name']: PetState(state, CONFIG_PATH) for state in config_obj["states"]}
        # Validate
        for state in states.values():
            for state in state.next_states.names:
                assert state in states

        pet = Pet(states, window)

        for event in config_obj["events"]:
            event_func = create_event_func(event, pet)
            if event["trigger"] == "click":
                window.bind("<Button-1>", event_func)

    # window configuration
    window.config(highlightbackground='black')
    label = tk.Label(window, bd=0, bg='black')
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor', 'black')
    label.pack()

    window.after(1, update)
    window.mainloop()

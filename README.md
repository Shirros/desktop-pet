# desktop-pet

![demo](click.gif)

Desktop pet using Python. Sprites in the assets folder are stolen from Nitrome. This project is based off of [this Medium post](https://medium.com/analytics-vidhya/create-your-own-desktop-pet-with-python-5b369be18868) but the code in that post is highly inflexible and a lot of things are hard coded.

My project has:

* Easy modification using JSON files
* OpenAI GPT support to turn your little friend into a helper that can answer your questions

## How to use

### Creating a pet config

Create a folder with a JSON file named `config.json` describing the pet, and all the gifs for your pet. The specifics of this JSON file are explained later. You can simply take one of the example configs I made in the `/assets/` folder in this repo. 

### Running the program

Clone this repo and run main.py OR download my totally safe exe (windows) or zip file (which macOS uses apparently?)

Run it like this: `python main.py /path/to/your/config/folder` or `& '.\desktop-pet.exe' C:\path\to\your\config\folder`

Suppose I downloaded the EXE and the `cave_chaos` folder from this repo. I put the `cave_chaos` folder in the same directory as the EXE. I can run it like this:

`& '.\desktop-pet.exe' cave_chaos`

### How to close

You can't close this program. That's not implemented yet. Just restart your PC or terminate the program in task manager. Sorry :)

### ChatGPT

I'm using the official openai API and not the unofficial chatgpt API because I don't want this repo to be taken down. It's easy to modify my program to use the unofficial API though.

If you want to use the openai feature, make sure you have an environmental variable `OPENAI_API_KEY` set to your openai API key

## How to get sprites from Nitrome (or any Flash game)

Get an SWF file from here:
https://archive.org/details/all_nitrome_games

Then decompile it using this tool
https://github.com/jindrapetrik/jpexs-decompiler
and extract all the image files. You can create gifs using ezgif or something.

## How to create your own pets

`config.json` looks like this:

```json
{
    "events": [...],
    "states": [...]
}
```

A list of events that can be triggered with your pet and a list of states your pet can be in.

Pets are finite state machines. This means that the "state" they are in follows a flow chart like this:

![FSM Diagram](fsm.jpg)

The states and transitions are defined in the JSON file. When left alone, the pet will randomly transition between these states.

This is an example of a state definition:

```json
{
    "state_name": "miner_tired",
    "dims": [0, 0, 45, 50], // [Offset the position by X horizontally, offset the position by X horizontally, width of the gif, height of the gif]
    "move": [2, 0], // Each frame, the pet will move [x, y] pixels
    "file_name": "miner_idle.gif",
    "transitions_to": [
        {
            "name": "miner_tired",
            "probability": 0.8 // 80% chance the pet will stay in the "tired" state every time the gif plays
        },
        {
            "name": "miner_sleeping",
            "probability": 0.2 // 20% chance the pet will start sleeping while being in the "tired" state
        }
    ]
},
```

This is an example of an event definition:

```json
{
    "trigger": "click",
    "type": "state_change",
    "new_state": "miner_mutating" // No matter what state the pet is in, when you click on it, it will forcibly change its state to "mutating"
}
```

```json
{
    "trigger": "click",
    "type": "chatgpt",
    "prompt": "Let’s chat.\nMe: %s\nYou:", // %s is where your message will be inserted
    "listen_state": "begin_listening", // It transitions to this state when you click on it
    "response_state": "begin_talking", // It transitions to this state when it starts talking
    "end_state": "idle" // It transitions to this state when it finishes talking
}
```

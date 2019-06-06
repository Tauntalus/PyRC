## PyRC
PyRC is an IRC server written in Python. It's built to be small, lightweight, and easily extensible.

# STATUS - IN DEVELOPMENT
PyRC is highly unstable and not particularly optimized right now. I'm currently working on getting the basic functionality of an IRC server implemented. It will likely not be ready for rollout for quite some time.

# HOW TO USE
PyRC runs on port 50625 by default. This can be changed in the main.py file to a port of your choosing. PyRC is ran via your python interpreter, simply enter a terminal, and run the command "python main.py" while in the project directory.

#KNOWN BUGS
Currently, PyRC is known to store the state of the users connected, but does not yet relay the messages back to the users who sent them.

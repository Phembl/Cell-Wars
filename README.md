# Cell Wars
Welcome to **Cell Wars**. 
<br>A two-player networked game based on cellular automata using Python and Pygame.

To run this game you will have to install Python version 3.8.10 plus pygame. After installing this you are able to run the game
via the console by navigating to /cell-wars/code and using the command **python3 run main.py**.

Upon starting the game you can select between:
<br>**Local Game**, **Host Game** and **Join Game**.

**Local Game** will run the game locally. Each player can be controlled by the same mouse and only inputs 
from the player whose turn it is are registered. This way the game can be played on one computer or even by only one person.

**Host Game** initializes a network and waits for another player (or instance) to join the session. The hosts IP address
is displayed.

**Join Game** prompts the user to input a target IP address. After entering the address the game starts on both the hosts and the joiners side.
<br> You can easily instanciate the game two times and test the network functionality this way.

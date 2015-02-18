Installation:

Run the following command to install dependencies:

sudo pip install -r requirements.txt


Make sure you have the required ssh keys installed in ~/.ssh on the machine
running this daemon. Check server_monitor.py for the full list.


Usage:

Run the server_monitor.py script with one of the following options:

    start   - If the monitor is not yet running it will be started.
    stop    - If the monitor is running it will be stopped.
    restart - This will attempt to stop the monitor and start it again.
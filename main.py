# This is the main file which starts the execution of the other compoennts
# The Flask and Django web servers run in separate threads
# The SMTP Relay Server runs in the main thread using an asynchronous event loop  

import asyncio
import threading
from relay import startRelayServer
from receiveMails import startReceiveMails
from djangoWeb.manage import main as startDjango
import subprocess

def runFlask():
    """This function starts up the Flask web server that receives incoming emails"""
    print("Starting flask app")
    startReceiveMails()

def runDjango():
    """This function starts up the Django web server that allows user registration"""
    print("Starting Django")
    # startDjango() (start the django development server for signup)
    subprocess.run(["python3", "djangoWeb/manage.py"])

if __name__ == '__main__':

    # Creating and starting a separate thread for the Flask application
    flaskThread = threading.Thread(target = runFlask)
    flaskThread.start()

    # Creating and starting a separate thread for the Django application
    djangoThread = threading.Thread(target = runDjango)
    djangoThread.start()

    # Creating and starting an event loop for the SMTP Relay Server
    loop = asyncio.get_event_loop()
    loop.create_task(startRelayServer())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Terminating program")

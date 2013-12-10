import os

from mlabwrap import mlab
from mlabraw import error as MatlabError

mlab.addpath(os.path.dirname(__file__))

from multiprocessing.connection import Listener, AuthenticationError

address = ('localhost', 7000)
listener = Listener(address, authkey='strumamor')
print "Listener created at", address

while True:
    try:
        connection = listener.accept()
    except AuthenticationError:
        continue
    print "Connection accepted from", listener.last_accepted

    try:
        path = connection.recv()
    except IOError as e:
        print "Connection receive error: %s" %(str(e))
        continue

    if path == "quit" or path == "exit":
        print "Received exit command."
        try:
            connection.send("Exited server.")
        finally:
            connection.close()
            break

    print "Received path", path    
    dir, file = os.path.split(path)

    try:
        data = mlab.extract_chord_features(dir + "/", file, 0, "")
    except MatlabError as e:
        data = "Error: %s" %(str(e))

    try:
        connection.send(data)
    except IOError as e:
        "Connection send error: %s" %(str(e))

    connection.close()
    print "Connection closed."

listener.close()

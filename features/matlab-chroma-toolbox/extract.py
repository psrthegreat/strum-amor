import os

from mlabwrap import mlab
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

    path = connection.recv()

    print "Received path", path

    if path == "quit":
        connection.close()
        break
    
    dir, file = os.path.split(path)
    data = mlab.extract_chord_features(dir + "/", file)

    connection.send(data)
    connection.close()

    print "Connection closed."

listener.close()

import os
from multiprocessing.connection import Client

def get_chroma(path):
    address = ("localhost", 7000)
    connection = Client(address, authkey='strumamor')
    connection.send(os.path.abspath(path))
    data = connection.recv()
    connection.close()
    return data

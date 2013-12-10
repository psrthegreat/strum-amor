import sys

path = sys.argv[1]

from multiprocessing.connection import Client
address = ("localhost", 7000)
connection = Client(address, authkey='strumamor')

connection.send(path)
data = connection.recv()
connection.close()

print data

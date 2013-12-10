"""
Simple IPC server to facilitate connection between Python
processes.

Usage:

    Server
    -------
    >>> def process(command):
    >>>     return 2
    >>> run_server(process)

    Client
    -------
    >>> conn = get_client()
    >>> conn.send("get answer")
    >>> print conn.recv()
    ... 2

"""
from multiprocessing.connection import (Client, Listener,
                                        AuthenticationError)

__address = ('localhost', 7000)
def get_client():
    """
    Gets client to communicate with listener.

    """
    return Client(__address, authkey='strumamor')

def get_response(command):
    """
    Gets data from server.

    """
    connection = get_client()

    connection.send(command)

    data = connection.recv()
    connection.close()

    return data

__quit_command = "quit"
def quit_server():
    """
    Quits server.

    """
    conn = get_client()
    conn.send(__quit_command)
    print conn.recv()
    conn.close()

def _process(connection, process):
    """
    Processes a server connection.

    """
    try:
        command = connection.recv()
    except IOError as e:
        return "Connection receive error: %s" %(str(e))

    if command == __quit_command:
        try:
            connection.send("Exited server.")
        finally:
            connection.close()
            return __quit_command

    print "Processing command", command
    data = process(command)

    try:
        connection.send(data)
    except IOError as e:
        return "Connection send error: %s" %(str(e))

    connection.close()

def run_server(process = lambda x : x):
    """
    Runs server (blocking).

    """
    print "Listener created at", __address
    listener = Listener(__address, authkey='strumamor')

    while True:
        try:
            connection = listener.accept()
        except AuthenticationError:
            continue
        print "Connection accepted from", listener.last_accepted

        result = _process(connection, process)

        if result == __quit_command:
            break

        if result is not None:
            print result

    listener.close()

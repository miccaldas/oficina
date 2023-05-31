"""
Module Docstring
"""
import snoop
from snoop import pp

# import os
# import subprocess
import socket


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


HOST = "localhost"
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
STATS = {
    "PUT": {"success": 0, "error": 0},
    "GET": {"success": 0, "error": 0},
    "GETLIST": {"success": 0, "error": 0},
    "PUTLIST": {"success": 0, "error": 0},
    "INCREMENT": {"success": 0, "error": 0},
    "APPEND": {"success": 0, "error": 0},
    "DELETE": {"success": 0, "error": 0},
    "STATS": {"success": 0, "error": 0},
}


@snoop
def server():
    """"""


if __name__ == "__main__":
    server()

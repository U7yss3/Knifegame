import socket
from _thread import *
import sys
"""pareil que pour metwork"""

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players_n = [('1'),('2')]
players_dat = [('0000'),('0000')]


def threaded_client(conn, player):
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            print("positions : ", players_dat)
            if data == "p":
                reply = players_n[player]
                players_dat[player] = "connected"
            else:
                print("data:", data)
                reply = players_dat[(player + 1) % 2]
                if data != "":
                    players_dat[player] = data

            if not data:
                print("Disconnected")
            else:
                print("Received by", player, " : ", data)
                print("Sending to", player, " : ",  reply)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr, "Player number ", currentPlayer)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = (currentPlayer + 1) % 2

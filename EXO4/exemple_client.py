import os, sys, socket

server = "51.38.191.157"
port = 12345

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	ma_socket.connect((server, port))
except Exception as e:
	print("Problème de connexion", e.args)
	sys.exit(1)

ligne = ma_socket.recv(1024)
print(ligne)

ma_socket.sendall(b"0000\n")
ligne = ma_socket.recv(1024)
print(ligne)

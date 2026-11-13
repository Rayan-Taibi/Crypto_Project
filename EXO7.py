
import socket
import string

server = "51.38.191.157"
port = 4321

nb_connexions = 500
longueur_message = 18

lettres_vues = [""] * longueur_message

for i in range(nb_connexions):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))

    message = s.recv(1024).decode().strip()
    s.close()

    for j in range(longueur_message):
        if message[j] not in lettres_vues[j]:
            lettres_vues[j] += message[j]

    if i % 50 == 0:
        print("Connexion numero", i)

message_secret = ""

for j in range(longueur_message):
    lettres_manquantes = ""

    for lettre in string.ascii_uppercase:
        if lettre not in lettres_vues[j]:
            lettres_manquantes += lettre

    if len(lettres_manquantes) == 1:
        message_secret += lettres_manquantes
    else:
        message_secret += "?"
        print("Position", j, ": plusieurs lettres manquantes")

print()
print("Message secret trouve :", message_secret)

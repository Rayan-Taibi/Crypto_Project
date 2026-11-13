
import socket

server = "51.38.191.157"
port = 23403


def recevoir(sock, marqueur):
    donnees = b""
    while marqueur.encode() not in donnees:
        donnees += sock.recv(4096)
    return donnees


def extraire(texte, marqueur, longueur):
    debut = texte.find(marqueur) + len(marqueur)
    return texte[debut:debut + longueur]


# Etape 1 : recuperer les anciennes valeurs

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((server, port))

recevoir(s1, "choice : ")
s1.sendall(b"1\n")

reponse = recevoir(s1, "here C =")
reponse += s1.recv(4096)

texte = reponse.decode()

challenge_old = extraire(texte, "challenge = ", 32)
iv_old = extraire(texte, "here IV = ", 32)
c = extraire(texte, "here C = ", 64)

print("Ancien challenge :", challenge_old)
print("Ancien IV :", iv_old)
print("C :", c)

s1.close()


# Etape 2 : recuperer le nouveau challenge

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((server, port))

recevoir(s2, "choice : ")
s2.sendall(b"2\n")

reponse = recevoir(s2, "IV")
texte = reponse.decode()

challenge_new = extraire(texte, "challenge : ", 32)

print("Nouveau challenge :", challenge_new)


# Etape 3 : calculer le nouvel IV

iv = bytes.fromhex(iv_old)
ancien = bytes.fromhex(challenge_old)
nouveau = bytes.fromhex(challenge_new)

nouvel_iv = b""

for i in range(16):
    valeur = iv[i] ^ ancien[i] ^ nouveau[i]
    nouvel_iv += bytes([valeur])

nouvel_iv = nouvel_iv.hex()

print("Nouvel IV :", nouvel_iv)


# Etape 4 : envoyer les valeurs

s2.sendall((nouvel_iv + "\n").encode())

reponse = s2.recv(4096)
print(reponse.decode())

s2.sendall((c + "\n").encode())

reponse = s2.recv(4096)
print(reponse.decode())

s2.close()

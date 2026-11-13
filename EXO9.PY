import socket

server = "51.38.191.157"
port = 11111

# les 3 blocs du fichier cbc_ciphertext (16 octets chacun)
iv = bytes.fromhex("d034423685a080a3521c6c7509dbeaeb")
c1 = bytes.fromhex("fb484eaaa0adcb76c712ee85d26913e2")
c2 = bytes.fromhex("d5a2d9101d0abc1c371152d49b04a7a4")

taille_bloc = 16


def recevoir_ligne(sock):
    # on lit jusqu'a trouver un retour a la ligne
    donnees = b""
    while b"\n" not in donnees:
        donnees = donnees + sock.recv(4096)
    return donnees.decode()


def demander_oracle(sock, deux_blocs):
    # deux_blocs = bloc_precedent (16 octets) + bloc_cible (16 octets)
    texte_hex = deux_blocs.hex()
    sock.sendall((texte_hex + "\n").encode())
    reponse = recevoir_ligne(sock)
    return "Successfully decrypted." in reponse


def attaquer_un_bloc(sock, bloc_precedent, bloc_cible):
    # intermediaire[i] = D_K(bloc_cible)[i], la sortie "brute" du dechiffrement AES
    # (avant le XOR avec le bloc precedent)
    intermediaire = [0] * taille_bloc
    clair = [0] * taille_bloc

    # on devine le padding "01", puis "02 02", puis "03 03 03", etc.
    for valeur_padding in range(1, taille_bloc + 1):

        position = taille_bloc - valeur_padding

        # on prepare un faux "bloc precedent" : pour toutes les positions
        # deja trouvees (a droite de "position"), on force le bon padding
        faux_bloc = [0] * taille_bloc
        for i in range(position + 1, taille_bloc):
            faux_bloc[i] = intermediaire[i] ^ valeur_padding

        octet_trouve = None

        for essai in range(256):
            faux_bloc[position] = essai

            essai_complet = bytes(faux_bloc) + bloc_cible
            padding_ok = demander_oracle(sock, essai_complet)

            if padding_ok:
                # cas particulier : pour le tout dernier octet (valeur_padding == 1),
                # il faut verifier que ce n'est pas un faux positif
                # (ca pourrait aussi etre un padding "02 02" par hasard)
                if valeur_padding == 1:
                    faux_bloc[position - 1] = faux_bloc[position - 1] ^ 0xFF
                    essai_verif = bytes(faux_bloc) + bloc_cible
                    toujours_ok = demander_oracle(sock, essai_verif)
                    faux_bloc[position - 1] = faux_bloc[position - 1] ^ 0xFF  # on annule

                    if not toujours_ok:
                        continue  # c'etait un faux positif, on continue a chercher

                octet_trouve = essai
                break

        intermediaire[position] = octet_trouve ^ valeur_padding
        clair[position] = intermediaire[position] ^ bloc_precedent[position]

        print("position", position, ": octet clair trouve =", chr(clair[position]) if 32 <= clair[position] < 127 else clair[position])

    return bytes(clair)


# ---------- attaque reelle ----------

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ma_socket.connect((server, port))

print("=== Attaque du bloc 1 (C1, dechiffre avec IV) ===")
p1 = attaquer_un_bloc(ma_socket, iv, c1)

print("")
print("=== Attaque du bloc 2 (C2, dechiffre avec C1) ===")
p2 = attaquer_un_bloc(ma_socket, c1, c2)

ma_socket.close()

message_complet = p1 + p2
print("")
print("Message complet (avec padding) :", message_complet)

# le dernier octet du message indique combien d'octets de padding enlever
nb_octets_padding = message_complet[-1]
message_final = message_complet[:-nb_octets_padding]

print("Message dechiffre final :", message_final.decode())
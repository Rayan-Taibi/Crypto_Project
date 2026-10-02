import hashlib
import time
hash_cible = '5a74dd4eef347734c8a0a9a3188abd11'
with open("rockyou.txt","r" , encoding="latin-1") as fichier:
    for mot_de_passe in fichier:
        mot_de_passe = mot_de_passe.strip() # ici strip supprime les espaces et les sauts de ligne
        hash_line = hashlib.md5(mot_de_passe.encode()).hexdigest() #conversion du mot de passe en hash md5
        if hash_line == hash_cible:
            print(f"Mot de passe trouve : {mot_de_passe}")
            break
    else:
        print("Mot de passe non trouve dans le fichier rockyou.txt")

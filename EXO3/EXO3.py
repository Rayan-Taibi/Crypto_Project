import zipfile
import itertools
import string
import zlib

def brute_force_zip(filename):
    alphabet = string.ascii_lowercase

    with zipfile.ZipFile(filename, "r") as archive:
        # On récupère le premier fichier contenu dans le ZIP
        fichier = archive.infolist()[0]

        longueur = 1

        while True:

            for combinaison in itertools.product(alphabet, repeat=longueur):
                password = ''.join(combinaison) #on convertit la combinaison en chaîne de caractères car itertools.product retourne un tuple ('a', 'b', 'c') par exemple)

                try:
                    with archive.open(fichier, pwd=password.encode()) as f:
                        f.read(1)

                    print(" Mot de passe trouve :", password)
                    return password

                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    # Mauvais mot de passe ou données compressées invalides
                    pass

            longueur += 1


brute_force_zip("archive.zip")
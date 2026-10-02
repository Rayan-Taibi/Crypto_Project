
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def chiffrer_cesar(texte, decalage):
    resultat = ""
    for lettre in texte:
        if lettre in alphabet:
            position = alphabet.index(lettre)
            nouvelle_position = (position + decalage) % 26
            resultat = resultat + alphabet[nouvelle_position]
        else:
            resultat = resultat + lettre
    return resultat

def dechiffrer_cesar(text , decalage):
    return chiffrer_cesar(text , -decalage)


def chiffrer_vigenere(texte, cle):
    resultat = ""
    index_cle = 0
    for lettre in texte:
        if lettre in alphabet:
            decalage = alphabet.index(cle[index_cle % len(cle)])
            position = alphabet.index(lettre)
            nouvelle_position = (position + decalage) %26
            resultat = resultat + alphabet[nouvelle_position]
            index_cle += 1  
        else:
            resultat = resultat + lettre    
    return resultat

def dechiffrer_vigenere(texte, cle):
    resultat = ""
    index_cle = 0
    for lettre in texte:
        if lettre in alphabet:
            decalage = alphabet.index(cle[index_cle % len(cle)])
            position = alphabet.index(lettre)
            nouvelle_position = (position - decalage) %26
            resultat = resultat + alphabet[nouvelle_position]
            index_cle += 1  
        else:
            resultat = resultat + lettre    
    return resultat




#================ Q2 ===============#


def nettoyer_text(texte):
    resultat = ""
    for lettre in texte:
        if lettre in alphabet:
            resultat = resultat + lettre
    return resultat

def frequence_lettre(texte):
    texte = nettoyer_text(texte)
    liste = []
    for lettre in alphabet:
        liste.append(100 *texte.count(lettre)/len(texte))
    return liste

#on va creer une fonction qui calcule l'indice de coincidence d'un texte qui sert

def indice_coincidence(texte):

    texte = nettoyer_text(texte)
    N = len(texte)
    somme = 0
    for lettre in alphabet:
        n = texte.count(lettre)
        somme +=  n*(n-1)

    return somme/(N*(N-1))

def trouve_decalage(texte):
    texte = nettoyer_text(texte)
    meilleure_lettre = 'a'
    maximum = 0
    for lettre in alphabet:
        if texte.count(lettre) > maximum:
            maximum  = texte.count(lettre)
            meilleure_lettre = lettre

    return alphabet.index(meilleure_lettre) - alphabet.index('e') % 26

def attaque_cesar(chiffre):
    decalage = trouve_decalage(chiffre)
    return decalage , dechiffrer_cesar(chiffre, decalage)




#================Q3==============#

def kasiski(chiffre):
    """Cherche les séquences de 3 lettres répétées, calcule les distances
    entre leurs apparitions, et compte pour chaque longueur L combien de
    distances sont des multiples de L."""
    chiffre = nettoyer_text(chiffre)
    distances = []
    for i in range(len(chiffre) - 2):
        motif = chiffre[i:i + 3]
        j = chiffre.find(motif, i + 1)      # prochaine apparition du motif
        if j != -1:
            distances.append(j - i)
    votes = {}
    for L in range(2, 21):
        votes[L] = 0
        for d in distances:
            if d % L == 0:
                votes[L] = votes[L] + 1
    return votes
 
def ic_moyen(chiffre, L):
    """IC moyen des L groupes (une lettre sur L)."""
    chiffre = nettoyer_text(chiffre)
    total = 0
    for i in range(L):
        total = total + indice_coincidence(chiffre[i::L])
    return total / L
 
def trouver_longueur_cle(chiffre):
    votes = kasiski(chiffre)
    maximum = max(votes.values())
    for L in range(2, 21):
        if votes[L] >= maximum / 2 and ic_moyen(chiffre, L) > 0.065:
            return L
    return 1
 
def attaque_vigenere(chiffre):
    L = trouver_longueur_cle(chiffre)
    chiffre = nettoyer_text(chiffre)
    cle = ""
    for i in range(L):
        groupe = chiffre[i::L]      # lettres chiffrées avec la même lettre de clé
        cle = cle + alphabet[trouve_decalage(groupe)]
    return cle, dechiffrer_vigenere(chiffre, cle)

        





if __name__ == "__main__":

    texte_original = "linspecteur ganimard examina la piece " \
    "avec une attention minutieuse la porte du coffrefort" \
    " avait ete forcee sans aucun bruit et le document confidentiel" \
    " concernant le plan de la banque avait disparu un seul indice " \
    "restait sur le bureau  un petit morceau de papier sur" \
    " lequel etait inscrite une suite de chiffres incomprehensible le" \
    " cambrioleur navait laisse aucune empreinte mais cette mysterieuse " \
    "note prouvait que le vol avait ete planifie depuis des semaines par" \
    " une personne connaissant parfaitement les lieux"





 
    print("Nombre de lettres :", len(nettoyer_text(texte_original)))
 
    c = chiffrer_cesar(texte_original, 3)
    print("Chiffre   :", c)
    print("\n")
    print("\n")
    
    print("Déchiffre :", dechiffrer_cesar(c, trouve_decalage(c)))
 
    print("\nFrequences des lettres du chiffre :")
    freq = frequence_lettre(c)
    for i in range(26):
        print(" ", alphabet[i], round(freq[i], 1), "%")
    print("IC du chiffre :", round(indice_coincidence(c), 4))
 
    k, clair = attaque_cesar(c)
    print("Attaque : décalage trouvé =", k)
    print("Texte retrouvé :", clair)

 




    v = chiffrer_vigenere(texte_original, "cle")
    
    print("Chiffré   :", v)
    print("Déchiffré :", dechiffrer_vigenere(v, "cle"))
    print("IC du chiffré :", round(indice_coincidence(v), 4))
    print("Votes Kasiski :", kasiski(v))
 
    cle, clair = attaque_vigenere(v)
    print("Attaque : clé trouvée =", cle)
    print("Texte retrouvé :", clair)
 


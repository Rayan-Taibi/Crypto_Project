
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
    freq = frequence_lettre(texte)
    meilleur_k = 0
    meilleur_score = -1
    for k in range(26):
        score = 0
        for i in range(26):
            score = score+ freq[i] * freq[(i+k)%26]
        if score > meilleur_score:
            meilleur_score = score
            meilleur_k = k  


    return meilleur_k

def attaque_cesar(chiffre):
    decalage = trouve_decalage(chiffre)
    return decalage , dechiffrer_cesar(chiffre, decalage)



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





 
    c = chiffrer_cesar(texte_original, 3)
    print("Cesar chiffre   :", c)
    print("Cesar déchiffre :", dechiffrer_cesar(c, 3))
 
    v = chiffrer_vigenere(texte_original, "cle")
    print("Vigenere chiffre   :", v)
    print("Vigenere déchiffre :", dechiffrer_vigenere(v, "cle"))

# Conception

- En cas de conflit de nom, le bot crée un fichier contenant ce qu'il aimerait écrire sur Wikipast (ancien + nouveau contenu).
- Limite de caractères pour le titre d'une œuvre : 150

Requête SPARQL utilisée sur data.bnf.fr/sparql :

    SELECT DISTINCT ?auteur WHERE
    {
        ?auteur foaf:focus ?identity.
        ?identity foaf:familyName ?nom.
    }


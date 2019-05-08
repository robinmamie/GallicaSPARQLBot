# Conception

- En cas de conflit de nom, le bot crée un fichier contenant ce qu'il aimerait écrire sur Wikipast. À vérifier individuellement en 2e pass.

Requête SPARQL utilisée sur data.bnf.fr/sparql :

    SELECT DISTINCT ?auteur WHERE
    {
        ?auteur foaf:focus ?identity.
        ?identity foaf:familyName ?nom.
    }


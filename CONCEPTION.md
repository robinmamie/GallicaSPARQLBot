# Conception

- Que faire en cas de conflit de nom ? Récupérer date de naissance et comparer, sinon drop ? Regarder s'il existe déjà un numéro BNF ?
- André Breton : des anciens bots ont laissé des données en-dessous. Proposition : récupération de la première liste uniquement pour la fusion des données.
- Lien Wikidata pour les œuvres ? Quelle référence ? (humains : Q5)

Requête SPARQL utilisée sur data.bnf.fr/sparql :

    SELECT DISTINCT ?auteur WHERE
    {
        ?auteur foaf:focus ?identity.
        ?identity foaf:familyName ?nom.
    }

- Exemples: Emile Zola, Claude Monet, Claude Gillot et Georges Delerue

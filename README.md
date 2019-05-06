# GallicaSPARQLBot

Le Gallica SPARQL bot est composé des fichiers suivants:

- `execute_bot.py`: à exécuter en utilisant `python execute_bot.py` pour créer la page de tous les auteurs présents sur Gallica.
- `bot_parsing.py`: parse les données présentes sur Gallica pour les présenter de façon standard sur WikiPast
- `web_tools.py`: contient les outils nécessaires pour récupérer et éditer diverses pages en ligne (wikipast, JSON, ...)
- `list_authors.py`: récupère le résultat de la commande SPARQL sauvegardée dans `data/authors_link.txt` afin de lister tous les auteurs dans le fichier `data/authors.txt`
- `data/authors_link.txt`: requête SPARQL de Gallica retournant un fichier JSON.
- `data/authors.txt`: éventuellement, liste de lien vers tous les auteurs listés sur Gallica (condition : doivent avoir un nom et un prénom!)
- `progress.py`: contient une barre de progression utile pour voir la progression du parsing des œuvres.
- `CONCEPTION.md`: discute des choix de conception du projet.

Exemple de texte affiché sur la console lorsque le fichier des liens des auteurs n'est pas encore présent :

    Dowloading JSON result from SPARQL request saved in data/authors_link.txt
    Parsing JSON result and saving it to data/authors.txt
    Reading links from data/authors.txt file
    Done

    * Author at index 0, 455150 to go
    Creating Louis-Florian-Paul Kergorlay
    ...

Exemple de texte affiché sur la console lorsque le fichier des liens des auteurs est déjà créé :

    Reading links from data/authors.txt file
    Done

    * Author at index 0, 455150 to go
    Creating Louis-Florian-Paul Kergorlay
    ...


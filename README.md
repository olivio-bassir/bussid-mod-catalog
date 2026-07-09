# bussid-mod-catalog

Catalogue public de l'application **Mod Studio BUSSID** (gestionnaire de mods pour Bus Simulator Indonesia).

- `catalog.json` — le catalogue consommé par l'appli (format documenté dans le README de l'appli).
- `liveries/` — liveries de **test** générées pour valider l'installation en un clic. Ce ne sont pas de vraies liveries adaptées aux templates UV des bus : elles servent à vérifier le pipeline téléchargement → galerie → picker in-game.

Les entrées « Maleo (officiel) » pointent vers les pages de téléchargement du site officiel bussimulator.id (leurs fichiers sont servis par des URLs expirantes, donc pas de lien direct possible).

## Ajouter un mod

1. Déposer le fichier (`.png`, `.bussidmod`, `.bussidvehicle`) dans le dossier adapté.
2. Ajouter une entrée dans `catalog.json` avec `fileUrl` pointant vers l'URL raw du fichier.
3. Commit + push : l'appli le voit au prochain rafraîchissement.

> Projet communautaire non affilié à Maleo. Ne publier ici que des fichiers dont vous détenez les droits.

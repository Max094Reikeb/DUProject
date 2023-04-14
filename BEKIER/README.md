# Prévisions Météo en France

Ce projet permet aux utilisateurs d'obtenir des prévisions météorologiques pour leur ville en France métropolitaine en sélectionnant leur région, département et ville. Les données météorologiques sont récupérées à partir d'une API dédiée et présentées de manière esthétique et ergonomique.

## Fonctionnalités

- Sélection de la région sur une carte interactive grâce aux balises HTML `map`, `usemap` et `area`
- Sélection du département et de la ville via des listes déroulantes
- Affichage des prévisions météo du jour pour la ville sélectionnée, ainsi que des prévisions pour les jours suivants
- Informations générales sur la ville, telles que l'heure de lever et de coucher du soleil et une carte des environs
- Personnalisation de l'affichage des prévisions météo, avec la possibilité de n'afficher que la tendance générale ou de consulter les prévisions par heure
- Sauvegarde des préférences de l'utilisateur et de la dernière ville consultée via des cookies
- Section "statistiques" affichant l'utilisation du site sous forme graphique, notamment le nombre total de visiteurs et le nombre de demandes d'informations météorologiques traitées au cours des derniers mois
- Mode clair et mode sombre pour l'interface utilisateur

## Installation et utilisation

1. Clonez ce dépôt sur votre machine locale.
2. Installez un serveur web local (comme [XAMPP](https://www.apachefriends.org/index.html) ou [WampServer](https://www.wampserver.com/)) et placez le projet dans le répertoire approprié (souvent `htdocs` ou `www`).
3. Démarrez votre serveur web local et accédez au projet via l'URL configurée (par exemple, `http://localhost/nom-du-dossier`).

## Technologies utilisées

- HTML, CSS et JavaScript pour la conception et l'interaction côté client
- PHP pour la gestion des requêtes et la récupération des données météorologiques
- [jQuery](https://jquery.com/) pour faciliter la manipulation du DOM et les requêtes AJAX
- API météorologique pour obtenir les données météorologiques en temps réel

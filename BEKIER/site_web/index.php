<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<h1>Prévisions météo en France</h1>
<!-- Ajout de la carte avec les régions -->
<?php include 'carte.php'; ?>

<!-- Formulaire pour sélectionner le département et la ville -->
<form id="form-meteo" action="meteo.php" method="post">
    <div id="select-departement">
        <!-- Le contenu sera ajouté en JavaScript -->
    </div>
    <div id="select-ville">
        <!-- Le contenu sera ajouté en JavaScript -->
    </div>
    <input type="submit" value="Voir la météo">
</form>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
</body>
</html>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<h1>Prévisions météo en France</h1>
<div class="container">
    <!-- On affiche la carte de la France avec les régions -->
    <?php include 'carte.php'; ?>

    <!-- Formulaire pour sélectionner le département et la ville -->
    <form id="form-meteo" action="meteo.php" method="post">
        <div id="select-department">
            <select disabled>
                <option value="">Sélectionnez un département</option>
            </select>
        </div>
        <div id="select-ville">
            <select disabled>
                <option value="">Sélectionnez une ville</option>
            </select>
        </div>
        <input type="hidden" name="ville" id="hidden-ville" value="">
        <input type="hidden" name="latitude" id="latitude">
        <input type="hidden" name="longitude" id="longitude">
        <input type="submit" value="Voir la météo" disabled>
    </form>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
</body>
</html>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<h1>Prévisions météo en France</h1>
<div class="main-container">
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
            <input type="hidden" id="ville" name="ville" value="">
            <input type="hidden" id="codePostal" name="codePostal">
            <input type="hidden" id="latitude" name="latitude">
            <input type="hidden" id="longitude" name="longitude">
            <input type="hidden" id="duration" name="duration"
                   value="<?php echo isset($_COOKIE['showPrevision']) ? $_COOKIE['showPrevision'] : '4_days'; ?>">
            <input type="submit" class="meteo-btn" value="Voir la météo" disabled>
        </form>
    </div>
    <!-- Bouton d'activation/de désactivation du dark mode -->
    <div class='toggle-switch'>
        <label>
            <input type='checkbox' id="theme-switcher">
            <span class='slider'></span>
        </label>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
</body>
</html>
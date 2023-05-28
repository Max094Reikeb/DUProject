<?php
// On définit la langue et le fuseau horaire
setlocale(LC_TIME, 'fr_FR.utf8', 'fra');
date_default_timezone_set('Europe/Paris');
$openWeatherApiKey = "b28fc63e0d3ce4e475038908516e8013";
// On récupère les informations des formulaires
$ville = $_POST['ville'];
$codePostal = $_POST['codePostal'];
$lat = $_POST['latitude'];
$lon = $_POST['longitude'];
$duration = $_POST['duration'];

// Appel de l'API OpenWeatherMap pour obtenir les données météo
$url = "https://api.openweathermap.org/data/3.0/onecall?lat={$lat}&lon={$lon}&exclude=minutely,alerts&units=metric&appid={$openWeatherApiKey}&lang=fr";
$response = file_get_contents($url);
$data = json_decode($response);

// On extrait les informations météo nécessaires
$currentWeather = $data->current;
// On prend les 4 prochain(e)s jours/heures
$forecast = $duration == '4_hours' ? array_slice($data->hourly, 1, 4) : array_slice($data->daily, 1, 4);

// On sauvegarde dans les cookies la ville, et les prévisions
setcookie('lastCity', $ville . " (" . $codePostal . ")", time() + (86400 * 30), '/');
setcookie('showPrevision', $duration, time() + (86400 * 30), '/');
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo de <?php echo $ville; ?></title>
    <link rel="stylesheet" href="css/style.css">
    <script src='https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css' rel='stylesheet'/>
</head>
<body>
<h1>Météo de <?php echo $ville; ?></h1>
<!-- Affichage de la dernière ville consultée (avec les cookies) -->
<?php
if (isset($_COOKIE['lastCity'])) {
    echo '<h4>Dernière ville consultée: ' . $_COOKIE['lastCity'] . '</h4>';
}
?>
<div class="main-container">
    <div class="container">
        <!-- Affichage des informations météo actuelles -->
        <div class="weather-info">
            <h2>
                Aujourd'hui, <?php
                $todayDate = new DateTime("@{$currentWeather->dt}");
                $todayDate->setTimezone(new DateTimeZone('Europe/Paris'));
                echo strftime("%A", $todayDate->getTimestamp());
                ?>
            </h2>
            <div class="weather-forecast">
                <img src="https://openweathermap.org/img/w/<?php echo $currentWeather->weather[0]->icon; ?>.png"
                     class="weather-icon" alt=""/> <span class="temp"><?php echo $currentWeather->temp; ?>°C</span>
            </div>
            <div class="infos">
                <div>Ressentie: <?php echo $currentWeather->feels_like; ?>°C</div>
                <div>Soleil: <?php
                    $sunRise = new DateTime("@{$currentWeather->sunrise}");
                    $sunSet = new DateTime("@{$currentWeather->sunset}");
                    $sunRise->setTimezone(new DateTimeZone('Europe/Paris'));
                    $sunSet->setTimezone(new DateTimeZone('Europe/Paris'));
                    echo $sunRise->format('H:i') . ' - ' . $sunSet->format('H:i');
                    ?>
                </div>
                <div>Humidité: <?php echo $currentWeather->humidity; ?> %</div>
                <div>Vent: <?php echo $currentWeather->wind_speed; ?> km/h</div>
                <div>Indice UV: <?php echo $currentWeather->uvi; ?></div>
            </div>
        </div>
        <!-- Affichage des informations météo futures (4 prochain(e)s jours/heures) -->
        <div class="forecast">
            <h2>Prévisions pour les 4 prochain<?php echo $duration == '4_hours' ? 'es heures' : 's jours'; ?></h2>
            <table>
                <thead>
                <tr>
                    <th><?php echo $duration == '4_hours' ? 'Heure' : 'Jour'; ?></th>
                    <th>Température moyenne</th>
                    <th>Prévision</th>
                </tr>
                </thead>
                <tbody>
                <?php foreach ($forecast as $time): ?>
                    <tr>
                        <td>
                            <?php
                            $date = new DateTime("@{$time->dt}");
                            $date->setTimezone(new DateTimeZone('Europe/Paris'));
                            echo $duration == '4_hours' ? $date->format('H:i') : strftime("%A", $date->getTimestamp());
                            ?>
                        </td>
                        <td><?php echo $duration == '4_hours' ? $time->temp : $time->temp->day; ?>°C</td>
                        <td><img src="https://openweathermap.org/img/w/<?php echo $time->weather[0]->icon; ?>.png"
                                 class="weather-icon" alt=""/></td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
            <!-- Bouton pour changer la préférence d'affichage de la météo future -->
            <form method="post" class="duration-form">
                <input type="hidden" name="ville" value="<?php echo $ville; ?>">
                <input type="hidden" name="codePostal" value="<?php echo $codePostal; ?>">
                <input type="hidden" name="latitude" value="<?php echo $lat; ?>">
                <input type="hidden" name="longitude" value="<?php echo $lon; ?>">
                <input type="hidden" name="duration"
                       value="<?php echo $duration == '4_days' ? '4_hours' : '4_days'; ?>">
                <button type="submit" class="switch-btn">Voir les 4
                    prochain<?php echo $duration == '4_days' ? 'es heures' : 's jours'; ?></button>
            </form>
        </div>
    </div>
    <!-- Bouton d'activation/de désactivation du dark mode -->
    <div class='toggle-switch'>
        <label>
            <input type='checkbox' id="theme-switcher">
            <span class='slider'></span>
        </label>
    </div>
</div>
<!-- Carte des environs de la ville sélectionnée -->
<div id='map'></div>
<!-- Bouton de retour à la sélection -->
<a href="index.php" class="back-btn">Retour à la sélection</a>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
<script>
    mapboxgl.accessToken = 'pk.eyJ1IjoibWF4MDk0cmVpa2ViIiwiYSI6ImNsaGx3dHRwazByNnczbG9waTlzdjBldDEifQ.nOQpjz8JlR8_jdAGFvg8lA';
    const map = new mapboxgl.Map({
        container: 'map', // id du conteneur HTML
        style: 'mapbox://styles/mapbox/streets-v11', // style de la carte
        center: [<?php echo str_replace(',', '.', $lon) . ', ' . str_replace(',', '.', $lat); ?>], // position initiale [longitude, latitude]
        zoom: 12 // niveau de zoom initial
    });
</script>
</body>
</html>
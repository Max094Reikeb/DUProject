<?php
setlocale(LC_TIME, 'fr_FR.utf8', 'fra'); // On définit la langue en Français (pour les noms des jours)
date_default_timezone_set('Europe/Paris'); // On définit notre fuseau horaire sur celui de Paris
$openWeatherApiKey = "b28fc63e0d3ce4e475038908516e8013";
$ville = $_POST['ville'];
$codePostal = $_POST['codePostal'];
$lat = $_POST['latitude'];
$lon = $_POST['longitude'];

// Appel de l'API OpenWeatherMap pour obtenir les données météo
$url = "https://api.openweathermap.org/data/3.0/onecall?lat={$lat}&lon={$lon}&exclude=minutely,hourly,alerts&units=metric&appid={$openWeatherApiKey}&lang=fr";
$response = file_get_contents($url);
$data = json_decode($response);

// Extraire les informations météo nécessaires
$currentWeather = $data->current;
$dailyWeather = array_slice($data->daily, 1, 7); // On prend les 7 prochains jours de prévision

// Sauvegarder la dernière ville consultée dans un cookie
setcookie('derniere_ville', $ville, time() + (86400 * 30), '/');
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
<div class="container">
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
            <div>Humidité: <?php echo $currentWeather->humidity; ?> %</div>
            <div>Vent: <?php echo $currentWeather->wind_speed; ?> km/h</div>
        </div>
    </div>
    <div class="forecast">
        <h2>Prévisions pour les 7 prochains jours</h2>
        <table>
            <thead>
            <tr>
                <th>Jour</th>
                <th>Température moyenne</th>
                <th>Prévision</th>
            </tr>
            </thead>
            <tbody>
            <?php foreach ($dailyWeather as $day): ?>
                <tr>
                    <td>
                        <?php
                        $date = new DateTime("@{$day->dt}");
                        $date->setTimezone(new DateTimeZone('Europe/Paris'));
                        echo strftime("%A", $date->getTimestamp());
                        ?>
                    </td>
                    <td><?php echo $day->temp->day; ?>°C</td>
                    <td><img src="https://openweathermap.org/img/w/<?php echo $day->weather[0]->icon; ?>.png"
                             class="weather-icon" alt=""/></td>
                </tr>
            <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>
<div id='map'></div>
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
<?php
$apiKey = "1c4adc203d26c4d319d106e37bd94148";
$ville = $_POST['ville'];
$lat = $_POST['latitude'];
$lon = $_POST['longitude'];

// Appel de l'API OpenWeatherMap pour obtenir les données météo
$url = "https://api.openweathermap.org/data/2.5/onecall?lat={$lat}&lon={$lon}&exclude=minutely,hourly,alerts&units=metric&appid={$apiKey}";
$response = file_get_contents($url);
$data = json_decode($response);

// Extraire les informations météo nécessaires
$currentWeather = $data->current;
$dailyWeather = $data->daily;

// Sauvegarder la dernière ville consultée dans un cookie
setcookie('derniere_ville', $ville, time() + (86400 * 30), '/');
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo de <?php echo $ville; ?></title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<h1>Météo de <?php echo $ville; ?></h1>
<p>Température actuelle : <?php echo $currentWeather->temp; ?>°C</p>
<p>Description : <?php echo $currentWeather->weather[0]->description; ?></p>
<p>Lever du soleil : <?php echo date('H:i', $currentWeather->sunrise); ?></p>
<p>Coucher du soleil : <?php echo date('H:i', $currentWeather->sunset); ?></p>

<h2>Prévisions pour les 7 prochains jours</h2>
<table>
    <thead>
    <tr>
        <th>Date</th>
        <th>Température</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($dailyWeather as $day): ?>
        <tr>
            <td><?php echo date('d/m/Y', $day->dt); ?></td>
            <td><?php echo $day->temp->day; ?>°C</td>
            <td><?php echo $day->weather[0]->description; ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>
<a href="index.php">Retour à la sélection</a>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
</body>
</html>
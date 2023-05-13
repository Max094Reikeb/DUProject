<?php
$apiKey = "b28fc63e0d3ce4e475038908516e8013";
$ville = $_POST['ville'];
$codePostal = $_POST['codePostal'];

// Appel de l'API OpenWeatherMap pour obtenir les données météo
$url = "http://api.openweathermap.org/data/2.5/forecast?zip={$codePostal},FR&units=metric&appid={$apiKey}&lang=fr";
$response = file_get_contents($url);
$data = json_decode($response);

// Extraire les informations météo nécessaires
$currentWeather = $data->list[0];
$dailyWeather = array_slice($data->list, 1, 7); // On prend les 7 prochains jours de prévision

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
<p>Température actuelle : <?php echo $currentWeather->main->temp; ?>°C</p>
<p>Description : <?php echo $currentWeather->weather[0]->description; ?></p>

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
            <td><?php echo $day->main->temp; ?>°C</td>
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
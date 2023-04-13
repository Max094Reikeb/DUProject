<?php
$apiKey = "1c4adc203d26c4d319d106e37bd94148";
$ville = $_POST['ville'];

// Appel de l'API OpenWeatherMap pour obtenir les données météo
$url = "https://api.openweathermap.org/data/2.5/weather?q={$ville},FR&units=metric&appid={$apiKey}";
$response = file_get_contents($url);
$data = json_decode($response);

// Extraire les informations météo nécessaires
$temperature = $data->main->temp;
$description = $data->weather[0]->description;
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
<p>Température : <?php echo $temperature; ?>°C</p>
<p>Description : <?php echo $description; ?></p>
<a href="index.php">Retour à la sélection</a>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="js/app.js"></script>
</body>
</html>
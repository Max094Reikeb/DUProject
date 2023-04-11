<?php
// Clé API
$api_key = '1c4adc203d26c4d319d106e37bd94148';

// Récupération des données d'entrée (régions, départements, villes)
$regions = array_map('str_getcsv', file('regions.csv'));
$departements = array_map('str_getcsv', file('departements.csv'));
$villes = array_map('str_getcsv', file('villes.csv'));

// Code HTML pour la carte interactive permettant de sélectionner la région
?>
<div>
    <h2>Sélectionnez votre région :</h2>
    <img src="img/region_map_france.png" usemap="#regions">
    <map name="regions">
        <area shape="poly" coords="..." href="page_meteo.php?region=1" alt="Auvergne-Rhône-Alpes">
        <area shape="poly" coords="..." href="page_meteo.php?region=2" alt="Bourgogne-Franche-Comté">
        <area shape="poly" coords="..." href="page_meteo.php?region=3" alt="Bretagne">
        <!-- ... -->
    </map>
</div>

<?php
// Sélection du département
if (isset($_GET['region'])) {
    $region_id = $_GET['region'];
    // Affichage des départements correspondants à la région sélectionnée
    ?>
    <div>
        <h2>Sélectionnez votre département :</h2>
        <ul>
            <?php
            // Obtention de la liste des départements de la région sélectionnée
            foreach ($departements as $departement) {
                if ($departement['region_id'] == $region_id) {
                    echo '<li><a href="page_meteo.php?region=' . $region_id . '&departement=' . $departement['id'] . '">' . $departement['nom'] . '</a></li>';
                }
            }
            ?>
        </ul>
    </div>
    <?php
}

// Sélection de la ville
if (isset($_GET['region']) && isset($_GET['departement'])) {
    $region_id = $_GET['region'];
    $departement_id = $_GET['departement'];
    // Affichage des villes correspondant au département sélectionné
    ?>
    <div>
        <h2>Sélectionnez votre ville :</h2>
        <select name="ville" onchange="location = this.value;">
            <?php
            // Obtention de la liste des villes du département sélectionné
            foreach ($villes as $ville) {
                if ($ville['departement_id'] == $departement_id) {
                    echo '<option value="page_meteo.php?region=' . $region_id . '&departement=' . $departement_id . '&ville=' . $ville['id'] . '">' . $ville['nom'] . '</option>';
                }
            }
            ?>
        </select>
    </div>
    <?php
}

// Code HTML pour afficher les informations météo de la ville sélectionnée
// if (isset($_GET['ville'])) {
// $ville_id = $_GET['ville'];
// Code PHP pour récupérer les informations météo de la ville sélectionnée
// Affichage des données
// Récupération des données météorologiques
// $weather_url = 'https://api.openweathermap.org/data/2.5/weather?q='.$ville_id.'&units=metric&appid='.$api_key;
// $weather_data = json_decode(file_get_contents($weather_url), true);
// $forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?q='.$ville_id.'&units=metric&appid='.$api_key;
// $forecast_data = json_decode(file_get_contents($forecast_url), true);
// $sun_url = 'https://api.sunrise-sunset.org/json?lat='.$weather_data['coord']['lat'].'&lng='.$weather_data['coord']['lon'].'&formatted=0';
// $sun_data = json_decode(file_get_contents($sun_url), true);

// Affichage de la météo
if (isset($_POST['ville'])) {
    $ville = $_POST['ville'];
    $meteo_url = 'https://api.openweathermap.org/data/2.5/weather?q='.$ville.'&units=metric&appid='.$api_key;
    $meteo = json_decode(file_get_contents($meteo_url), true); // fonction qui récupère les données météo du site dédié
    // Affichage des prévisions du jour
    echo "<h2>Aujourd'hui à ".$ville." : ".$meteo['conditions']."</h2>";
    echo "<p>Température : ".$meteo['temperature']." °C</p>";
    echo "<p>Vitesse du vent : ".$meteo['vent']." km/h</p>";
    // Affichage des prévisions pour les jours suivants
    echo "<h3>Prévisions pour les prochains jours :</h3>";
    echo "<ul>";
    foreach ($meteo['previsions'] as $jour => $previsions) {
        echo "<li>".$jour." : ".$previsions['conditions'].", ".$previsions['temperature']." °C</li>";
    }
    echo "</ul>";
} else {
    echo "<p>Veuillez sélectionner une ville pour afficher la météo.</p>";
}

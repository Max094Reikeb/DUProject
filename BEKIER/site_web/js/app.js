$(document).ready(function () {
    // Gestion de la sélection de la région, département et ville
    const $selectDepartment = $('#select-department select');
    const $selectVille = $('#select-ville select');
    const $submitButton = $('#form-meteo input[type="submit"]');
    const $inputVille = $('#ville');
    const $inputCodePostal = $('#codePostal');
    const $inputLatitude = $('#latitude');
    const $inputLongitude = $('#longitude');

    // Fonction permettant d'obtenir les villes d'un département, avec l'API geo.api.gouv.fr
    function updateVilles(departmentCode) {
        const url = `https://geo.api.gouv.fr/departements/${departmentCode}/communes?fields=nom,codesPostaux,centre`;

        $.getJSON(url, function (data) {
            let options = '<option value="">Sélectionnez une ville</option>';

            data.forEach(function (ville) {
                options += `<option value="${ville.nom},${ville.codesPostaux[0]},${ville.centre.coordinates[1]},${ville.centre.coordinates[0]}">${ville.nom}</option>`;
            });

            $selectVille.html(options).prop('disabled', false);
        });
    }

    // Sélection du département
    $selectDepartment.on('change', function () {
        const departement = $(this).val();
        if (departement) {
            updateVilles(departement);
        } else {
            $selectVille.prop('disabled', true).val('');
        }
        $submitButton.prop('disabled', true);
    });

    // Sélection de la ville
    $selectVille.on('change', function () {
        const [ville, codePostal, latitude, longitude] = $(this).val().split(',');
        if (ville) {
            $inputVille.val(ville);
            $inputCodePostal.val(codePostal);
            $inputLatitude.val(latitude);
            $inputLongitude.val(longitude);
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    });
});

// Gestion du mode sombre
// On vérifie si le mode sombre est enregistré
if (localStorage.getItem('dark-mode') === 'true') {
    document.body.classList.add('dark-mode');
    $('.meteo-btn').addClass('dark-mode');
    $('.switch-btn').addClass('dark-mode');
}

// On change le mode avec le switch
document.getElementById('theme-switcher').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    $('.meteo-btn').toggleClass('dark-mode');
    $('.switch-btn').toggleClass('dark-mode');

    // On enregistre dans le local storage
    localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode').toString());
});

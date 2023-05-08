$(document).ready(function () {
    // Gestion de la sélection de la région, département et ville
    const $selectDepartment = $('#select-department select');
    const $selectVille = $('#select-ville select');
    const $latitudeInput = $('#latitude');
    const $longitudeInput = $('#longitude');
    const $submitButton = $('#form-meteo input[type="submit"]');

    // Fonction permettant d'obtenir les villes d'un département, avec l'API geo.api.gouv.fr
    function updateVilles(departmentCode) {
        const url = `https://geo.api.gouv.fr/departements/${departmentCode}/communes?fields=nom,code,centre`;

        $.getJSON(url, function (data) {
            let options = '<option value="">Sélectionnez une ville</option>';

            data.forEach(function (ville) {
                options += `<option value="${ville.nom}" data-lat="${ville.centre.coordinates[1]}" data-lon="${ville.centre.coordinates[0]}">${ville.nom}</option>`;
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
        const ville = $(this).val();
        if (ville) {
            const selectedOption = $(this).find('option:selected');
            const lat = selectedOption.data('lat');
            const lon = selectedOption.data('lon');
            $latitudeInput.val(lat);
            $longitudeInput.val(lon);
            $submitButton.prop('disabled', false);
            $('#hidden-ville').val(ville);
        } else {
            $latitudeInput.val('');
            $longitudeInput.val('');
            $submitButton.prop('disabled', true);
        }
    });
});
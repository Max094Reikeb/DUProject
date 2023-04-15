$(document).ready(function () {
    // Gestion de la sélection de la région, département et ville en JavaScript
    const $selectDepartment = $('#select-department select');
    const $selectVille = $('#select-ville select');
    const $submitButton = $('#form-meteo input[type="submit"]');

    function updateVilles(departmentCode) {
        const url = `https://geo.api.gouv.fr/departements/${departmentCode}/communes?fields=nom`;

        $.getJSON(url, function (data) {
            let options = '<option value="">Sélectionnez une ville</option>';

            data.forEach(function (ville) {
                options += `<option value="${ville.nom}">${ville.nom}</option>`;
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
            $submitButton.prop('disabled', false);
        } else {
            $submitButton.prop('disabled', true);
        }
    });
});
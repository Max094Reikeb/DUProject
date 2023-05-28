// Fonction permettant d'obtenir les départements d'une région, avec l'API geo.api.gouv.fr
function updateDepartements(region) {
    const url = `https://geo.api.gouv.fr/regions/${region}/departements?fields=nom,code`;

    $.getJSON(url, function (data) {
        let options = '<option value="">Sélectionnez un département</option>';

        data.forEach(function (departement) {
            options += `<option value="${departement.code}">${departement.nom} (${departement.code})</option>`;
        });

        $('#select-department select').html(options).prop('disabled', false);
    });
}

// Fonction permettant de gérer la sélection des régions en détectant les clics sur la carte.
document.querySelectorAll('area').forEach(area => {
    area.addEventListener('click', (e) => {
        e.preventDefault();
        const region = e.target.dataset.region;
        // Met à jour les départements dans la liste déroulante correspondante.
        updateDepartements(region);
    });
});
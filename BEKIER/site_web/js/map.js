// Fonction permettant d'obtenir les départements d'une région, avec l'API geo.api.gouv.fr
function updateDepartements(region) {
    const url = `https://geo.api.gouv.fr/regions/${region}/departements?fields=nom,code`;

    $.getJSON(url, function (data) {
        let options = '<option value="">Sélectionnez un département</option>';

        data.forEach(function (departement) {
            options += `<option value="${departement.code}">${departement.nom}</option>`;
        });

        $('#select-department select').html(options).prop('disabled', false);
    });
}

document.querySelectorAll('area').forEach(area => {
    area.addEventListener('click', (e) => {
        e.preventDefault();
        const region = e.target.dataset.region;
        updateDepartements(region);
    });
});
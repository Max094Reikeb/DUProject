const regions = {
    "auvergne-rhone-alpes": {
        departements: {
            "01": "Ain",
            "03": "Allier",
            "07": "Ardèche",
            "15": "Cantal",
            "26": "Drôme",
            "38": "Isère",
            "42": "Loire",
            "43": "Haute-Loire",
            "63": "Puy-de-Dôme",
            "69": "Rhône",
            "73": "Savoie",
            "74": "Haute-Savoie"
        }
    },
    "bourgogne-franche-comte": {
        departements: {
            "21": "Côte-d'Or",
            "25": "Doubs",
            "39": "Jura",
            "58": "Nièvre",
            "70": "Haute-Saône",
            "71": "Saône-et-Loire",
            "89": "Yonne",
            "90": "Territoire de Belfort"
        }
    },
    "bretagne": {
        departements: {
            "22": "Côtes-d'Armor",
            "29": "Finistère",
            "35": "Ille-et-Vilaine",
            "56": "Morbihan"
        }
    },
    "centre-val-de-loire": {
        departements: {
            "18": "Cher",
            "28": "Eure-et-Loir",
            "36": "Indre",
            "37": "Indre-et-Loire",
            "41": "Loir-et-Cher",
            "45": "Loiret"
        }
    },
    "corse": {
        departements: {
            "2A": "Corse-du-Sud",
            "2B": "Haute-Corse"
        }
    },
    "grand-est": {
        departements: {
            "08": "Ardennes",
            "10": "Aube",
            "51": "Marne",
            "52": "Haute-Marne",
            "54": "Meurthe-et-Moselle",
            "55": "Meuse",
            "57": "Moselle",
            "67": "Bas-Rhin",
            "68": "Haut-Rhin",
            "88": "Vosges"
        }
    },
    "hauts-de-france": {
        departements: {
            "02": "Aisne",
            "59": "Nord",
            "60": "Oise",
            "62": "Pas-de-Calais",
            "80": "Somme"
        }
    },
    "ile-de-france": {
        departements: {
            "75": "Paris",
            "77": "Seine-et-Marne",
            "78": "Yvelines",
            "91": "Essonne",
            "92": "Hauts-de-Seine",
            "93": "Seine-Saint-Denis",
            "94": "Val-de-Marne",
            "95": "Val-d'Oise"
        }
    },
    "normandie": {
        departements: {
            "14": "Calvados",
            "27": "Eure",
            "50": "Manche",
            "61": "Orne",
            "76": "Seine-Maritime"
        }
    },
    "nouvelle-aquitaine": {
        departements: {
            "16": "Charente",
            "17": "Charente-Maritime",
            "19": "Corrèze",
            "23": "Creuse",
            "24": "Dordogne",
            "33": "Gironde",
            "40": "Landes",
            "47": "Lot-et-Garonne",
            "64": "Pyrénées-Atlantiques",
            "79": "Deux-Sèvres",
            "86": "Vienne",
            "87": "Haute-Vienne"
        }
    },
    "occitanie": {
        departements: {
            "09": "Ariège",
            "11": "Aude",
            "12": "Aveyron",
            "30": "Gard",
            "31": "Haute-Garonne",
            "32": "Gers",
            "34": "Hérault",
            "46": "Lot",
            "48": "Lozère",
            "65": "Hautes-Pyrénées",
            "66": "Pyrénées-Orientales",
            "81": "Tarn",
            "82": "Tarn-et-Garonne"
        }
    },
    "pays-de-la-loire": {
        departements: {
            "44": "Loire-Atlantique",
            "49": "Maine-et-Loire",
            "53": "Mayenne",
            "72": "Sarthe",
            "85": "Vendée"
        }
    },
    "provence-alpes-cote-dazur": {
        departements: {
            "04": "Alpes-de-Haute-Provence",
            "05": "Hautes-Alpes",
            "06": "Alpes-Maritimes",
            "13": "Bouches-du-Rhône",
            "83": "Var",
            "84": "Vaucluse"
        }
    }
};

function updateDepartements(region) {
    const departements = regions[region].departements;
    let options = '<select name="departement"><option value="">Sélectionnez un département</option>';

    for (const [code, nom] in Object.entries(departements)) {
        options += `<option value="${code}">${nom}</option>`;
    }

    options += '</select>';

    document.getElementById('select-departement').innerHTML = options;
}

document.querySelectorAll('area').forEach(area => {
    area.addEventListener('click', (e) => {
        e.preventDefault();
        const region = e.target.dataset.region;
        updateDepartements(region);
    });
});
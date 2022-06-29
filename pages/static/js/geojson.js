class AddressSuggestion {
    minLength = 3;
    address = null;
    timer = null;
    suggestions = null;
    request = 0;
    country = '';
    api = 'https://nominatim.openstreetmap.org/search?format=geojson&limit=5&country=BY';
    requestParams = {
        headers: {
            'accept-language': 'ru-RU',
        },
    };

    constructor(element) {
        this.element = element;
        this.citiesHTML = document.getElementById('cities');
        this.geoID = document.getElementById('id_geo_id');
        this.initEvents();
    }
    initEvents() {
        if (this.element) {
            this.element.addEventListener('input', this.debounceRequest);
        }
        if (this.citiesHTML) {
            this.citiesHTML.addEventListener('click', (e) => {
                this.suggestions = null;
                this.resetList();
                this.element.value = e.target.innerText;
                this.geoID.value = e.target.getAttribute('data-osm_id');
            });
        }
    }
    debounceRequest = () => {
        if (this.timer) {
            this.timer = clearTimeout(this.timer);
        }
        if (this.element.value.trim().length < this.minLength) {
            this.resetList();
            return false;
        }
        this.timer = setTimeout(async () => {
            await this.sendRequest();
            await this.repaint();
        }, 300);
    }
    sendRequest = async () => {
        const city = this.element.value;
        this.suggestions = await fetch(`${this.api}&city=${encodeURI(city)}`, this.requestParams)
            .then(response => {
                return response.json();
            });
        this.request++;
    }
    repaint = (extraHTML=null) => {
        if (extraHTML) {
            this.citiesHTML.innerHTML = '';
            return true;
        }
        let list = '';
        if (this.suggestions?.features) {
            for (let feature of this.suggestions.features) {
                list += `<li data-osm_id="${feature.properties.osm_id}">${feature.properties.display_name}</li>`;
            }
        }
        if (list.length) {
            return this.citiesHTML.innerHTML = list;
        }
        return this.citiesHTML.innerHTML = '<li class="disabled">Не найдено...</li>'
    }
    resetList() {
        this.suggestions = null;
        this.repaint(true);
    }
}
const Suggestion = new AddressSuggestion(document.getElementById('id_city'));
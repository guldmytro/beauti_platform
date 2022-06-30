class AddressSuggestion {
    minLength = 3;
    address = null;
    timer = null;
    suggestions = null;
    currentCity = '';
    request = 0;
    country = '';
    api = 'https://nominatim.openstreetmap.org/search?format=geojson&limit=5&country=BY';
    addressApi = 'https://nominatim.openstreetmap.org/lookup';
    requestParams = {
        headers: {
            'accept-language': 'ru-RU',
        },
    };
    constructor(cityElement, addressElement) {
        this.element = cityElement;
        this.addressElement = addressElement;
        this.citiesHTML = document.getElementById('cities');
        this.addressHTML = document.getElementById('addresses');
        this.geoID = document.getElementById('id_geo_id');
        this.addressID = document.getElementById('id_address_id');
        this.initEvents();
        if (!this.addressElement.value) {
            this.hideAddressField();
        }
    }
    initEvents() {
        if (this.element) {
            this.element.addEventListener('input', this.debounceRequest.bind(this, this.citiesHTML, this.element));
            this.addressElement.addEventListener('input', this.debounceRequest.bind(this, this.addressHTML, this.addressElement));
            this.element.addEventListener('keyup', this.resetField);
            this.element.addEventListener('touchend', this.resetField);
        }
        if (this.citiesHTML) {
            this.citiesHTML.addEventListener('click', (e) => {
                this.suggestions = null;
                this.resetList(false, this.citiesHTML);
                const osmId = e.target.getAttribute('data-osm_id');
                if (osmId) {
                    this.element.value = e.target.innerText;
                    this.geoID.value = osmId;
                    this.setCurrentCity();
                    this.showAddressField();
                } else {
                    this.hideAddressField();
                }
            });
        }
        if (this.addressHTML) {
            this.addressHTML.addEventListener('click', (e) => {
                this.suggestions = null;
                this.resetList(false, this.addressHTML);
                const osmId = e.target.getAttribute('data-osm_id');
                if (osmId) {
                    this.addressElement.value = e.target.innerText;
                    this.addressID.value = osmId;
                }
            });
        }
    }
    resetField = () => {
        this.geoID.value = '';
        this.hideAddressField();
        this.resetCurrentCity();
    }
    setCurrentCity = () => {
        this.currentCity = String(this.element.value).split(',')[0];
    }
    resetCurrentCity = () => {
        this.currentCity = false;
    }
    hideAddressField = () => {
        this.addressElement.closest('.popup__group').style.display = 'none';
        this.addressElement.value = '';
    }
    showAddressField = () => {
        this.addressElement.closest('.popup__group').style.display = 'block';
        this.addressElement.value = '';
        this.addressElement.focus();
    }
    debounceRequest = (list, target) => {
        if (this.timer) {
            this.timer = clearTimeout(this.timer);
        }
        if (target.value.trim().length < this.minLength) {
            this.resetList();
            return false;
        }
        this.timer = setTimeout(async () => {
            await this.sendRequest();
            this.repaint(false, list);
            console.log(target);
        }, 300);
    }
    sendRequest = async () => {
        const city = this.currentCity  || this.element.value.split(',')[0];
        const address = this.addressElement.value;
        this.suggestions = await fetch(`${this.api}&city=${encodeURI(city)}&street=${address}`, this.requestParams)
            .then(response => {
                return response.json();
            });
        this.request++;
    }
    repaint = (extraHTML=null, element) => {
        if (extraHTML) {
            this.citiesHTML.innerHTML = '';
            this.addressHTML.innerHTML = '';
            return true;
        }
        let list = '';
        if (this.suggestions?.features) {
            for (let feature of this.suggestions.features) {
                list += `<li data-osm_id="${feature.properties.osm_id}">${feature.properties.display_name}</li>`;
            }
        }
        if (list.length) {
            return element.innerHTML = list;
        }
        return element.innerHTML = '<li class="disabled">Не найдено...</li>'
    }
    resetList() {
        this.suggestions = null;
        this.repaint(true);
    }
}
const Suggestion = new AddressSuggestion(document.getElementById('id_city'), document.getElementById('id_address'));
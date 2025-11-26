// app.js

function searchCity() {
    const city = document.getElementById("cityInput").value.trim();

    if (city === "") {
        alert("Podaj nazwę miasta!");
        return;
    }

    // ZMIANA: Dodano &limit=30
    const url = `https://api.api-ninjas.com/v1/city?name=${city}`;

    // Pamiętaj, aby wpisać tutaj swój prawdziwy klucz API zamiast "temp"
    fetch(url, {
        headers: { "X-Api-Key": "4LlgASu82AwBAUyb3EEgOg==Ft6GGyMgwCJfie9F" }
    })
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error(error));
}

function displayResults(cities) {
    console.log("Dane z API:", cities); // To pokaże w konsoli co dokładnie przyszło

    const list = document.getElementById("resultList");
    list.innerHTML = ""; // czyścimy poprzednie wyniki

    // SPRAWDZENIE: Czy otrzymaliśmy tablicę?
    if (!Array.isArray(cities)) {
        // Jeśli to nie tablica, to pewnie obiekt błędu (np. złe API Key)
        console.error("To nie jest tablica:", cities);
        list.innerHTML = `< li style = "color: red;" > Wystąpił błąd API.Sprawdź konsolę (F12).< br > Komunikat: ${JSON.stringify(cities)}</li > `;
        return;
    }

    if (cities.length === 0) {
        list.innerHTML = "<li>Brak wyników.</li>";
        return;
    }

    cities.forEach(city => {

        const li = document.createElement("li");
        li.textContent = `${city.name}, ${city.country} – populacja: ${city.population} `;
        const temp = city;
        // Opcjonalnie: Przycisk mapy (jeśli chcesz go dodać)
        const btn = document.createElement("button");
        btn.textContent = "Pokaż";
        btn.style.marginLeft = "10px";
        btn.onclick = () => {
            const airUrl = `https://api.api-ninjas.com/v1/airquality?city=${encodeURIComponent(city.name)}`;
            const tempUrl = `https://api.api-ninjas.com/v1/weather?lat=${encodeURIComponent(city.latitude)}&lon=${encodeURIComponent(city.longitude)}`; // lub Twój tempUrl

            // Pobieramy równocześnie PM i temperaturę
            Promise.all([
                fetch(airUrl, { headers: { "X-Api-Key": "4LlgASu82AwBAUyb3EEgOg==Ft6GGyMgwCJfie9F" } }).then(res => res.json()),
                fetch(tempUrl, { headers: { "X-Api-Key": "4LlgASu82AwBAUyb3EEgOg==Ft6GGyMgwCJfie9F" } }).then(res => res.json())
            ])
                .then(([airData, tempData]) => {
                    console.log("Air quality:", airData);
                    console.log("Temperature:", tempData);

                    if (window.map) {
                        const marker = L.marker([city.latitude, city.longitude]).addTo(window.map);

                        const pm10 = airData["PM10"]?.concentration ?? "brak danych";
                        const pm25 = airData["PM2.5"]?.concentration ?? "brak danych";
                        const temp = tempData.temp ?? "brak danych";

                        const popupContent = `
                <b>${city.name}</b><br>
                PM10: ${pm10}<br>
                PM2.5: ${pm25}<br>
                Temperatura: ${temp}°C
            `;
                        marker.bindPopup(popupContent).openPopup();
                        window.map.setView([city.latitude, city.longitude], 12);
                    }
                })
                .catch(error => console.error(error));
        };


        li.appendChild(btn);

        list.appendChild(li);
    });
}
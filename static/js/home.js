// Ecllipse of API key
function showContent(event) {
    event.preventDefault();

    var inputText = document.getElementById('openaiKey').value;
    var outputElement = document.getElementById('output');
    var maxLength = 15;

    outputElement.innerText = inputText;

    if (inputText.length > maxLength) {
        var visibleText = inputText.substring(0, maxLength / 2) + "...";
        var remainingText = inputText.substring(inputText.length - maxLength / 2);
        outputElement.innerText = visibleText + remainingText;
    }

    document.getElementById('openai-form').reset();
}

// Clear the output
function clearOutput() {
    document.getElementById('output').innerHTML = '';
}

// Weather card data
document.addEventListener("DOMContentLoaded", function () {
    function getDate() {
        const date = new Date();
        const options = { weekday: 'short', month: '2-digit', day: '2-digit' };
        return date.toLocaleDateString('en-US', options);
    }

    function fetchWeather(latitude, longitude) {
        const apiKey = 'API'; // Replace with your OpenWeatherMap API key
        const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const temperature = Math.round(data.main.temp);
                const weatherDescription = data.weather[0].description;
                document.getElementById('temperature').textContent = `${temperature}°C`;
                document.getElementById('weather').textContent = weatherDescription;
            })
            .catch(error => console.log('Error fetching weather data:', error));
    }

    document.getElementById('date').textContent = getDate();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            fetchWeather(latitude, longitude);
        }, error => {
            console.log('Error getting location:', error);
            document.getElementById('temperature').textContent = 'Error fetching weather data';
        });
    } else {
        console.log('Geolocation is not supported by this browser.');
        document.getElementById('temperature').textContent = 'Geolocation is not supported by this browser.';
    }
});
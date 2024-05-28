const timeEl = document.getElementById('time');
const dateEl = document.getElementById('date');
const currentWeatherItemsEl = document.getElementById('current-weather-items');
const timezone = document.getElementById('time-zone');
const countryEl = document.getElementById('country');
const weatherForecastEl = document.getElementById('weather-forecast');
const currentTempEl = document.getElementById('current-temp');


const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const API_KEY ='49cc8c821cd2aff9af04c9f98c36eb74';

setInterval(() => {
    const time = new Date();
    const month = time.getMonth();
    const date = time.getDate();
    const day = time.getDay();
    const hour = time.getHours();
    const hoursIn12HrFormat = hour >= 13 ? hour %12: hour
    const minutes = time.getMinutes();
    const ampm = hour >=12 ? 'PM' : 'AM'

    timeEl.innerHTML = (hoursIn12HrFormat < 10? '0'+hoursIn12HrFormat : hoursIn12HrFormat) + ':' + (minutes < 10? '0'+minutes: minutes)+ ' ' + `<span id="am-pm">${ampm}</span>`

    dateEl.innerHTML = days[day] + ', ' + date+ ' ' + months[month]

}, 1000);

getWeatherData()
function getWeatherData () {
    navigator.geolocation.getCurrentPosition((success) => {

        let {latitude, longitude } = success.coords;

        fetch(`https://api.openweathermap.org/data/2.5/onecall?lat=${latitude}&lon=${longitude}&exclude=hourly,minutely&units=metric&appid=${API_KEY}`).then(res => res.json()).then(data => {

        console.log(data)
        showWeatherData(data);
        })

    })
}

// Function to show weather data along with farm activity suggestions
function showWeatherData(data) {
    let { humidity, pressure, sunrise, sunset, wind_speed, weather } = data.current;

    // Display weather information
    timezone.innerHTML = 'Time Zone : '+data.timezone + ' (UTC' + (data.timezone_offset >= 0 ? '+' : '') + (data.timezone_offset / 3600) + ')';
    countryEl.innerHTML = 'Longitude : '+data.lat + 'N ' + 'and Latitude : '+data.lon + 'E';

    currentWeatherItemsEl.innerHTML =
        `<div class="weather-item">
            <div>Humidity</div>
            <div>${humidity}%</div>
        </div>
        <div class="weather-item">
            <div>Pressure</div>
            <div>${pressure}</div>
        </div>
        <div class="weather-item">
            <div>Wind Speed</div>
            <div>${wind_speed}</div>
        </div>
        <div class="weather-item">
            <div>Sunrise</div>
            <div>${window.moment(sunrise * 1000).format('HH:mm a')}</div>
        </div>
        <div class="weather-item">
            <div>Sunset</div>
            <div>${window.moment(sunset * 1000).format('HH:mm a')}</div>
        </div>`;

    // Determine farm activities based on weather conditions
    let activitySuggestions = [];
    if (weather[0].main === 'Rain') {
        activitySuggestions.push("Consider focusing on indoor tasks like sorting seeds, cleaning equipment, and planning future activities.");
    } else if (weather[0].main === 'Clear') {
        activitySuggestions.push("It's a good day for fieldwork like planting seeds, transplanting seedlings, and general farm maintenance.");
    } else if (weather[0].main === 'Clouds') {
        activitySuggestions.push("You can perform various tasks today. Check your equipment, maintain fences, or prepare for upcoming tasks.");
    }else if (weather[0].main === 'Haze') {
        activitySuggestions.push("During hazy weather, it's advisable to avoid strenuous outdoor activities. Focus on indoor tasks like inventory management, equipment maintenance, and planning.");
    }
     else {
        console.log(weather[0].main)
        activitySuggestions.push("Evaluate the weather conditions to determine suitable farm activities for the day.");
    }

    // Display farm activity suggestions
    activitySuggestions.forEach(activity => {
        currentWeatherItemsEl.innerHTML += `
            <div class="weather-item">
                <div style="font-size:2em;">Farm Activity:&nbsp;&nbsp</div>
                <br>
                
            </div>
            <div><strong>${activity}</strong></div>`;
    });

    // Display weather forecast for upcoming days
    let otherDayForcast = '';
    data.daily.forEach((day, idx) => {
        if (idx === 0) {
            currentTempEl.innerHTML = `
            <img src="http://openweathermap.org/img/wn/${day.weather[0].icon}@4x.png"
            alt="weather icon" class="w-icon">
            <div class="other">
                <div class="day">${window.moment(day.dt * 1000).format('dddd')}</div>
                <div class="temp">Night - ${day.temp.night}&#176;C</div>
                <div class="temp">Day - ${day.temp.day}&#176;C</div>
            </div>`;
        } else {
            otherDayForcast += `
            <div class="weather-forecast-item">
                <div class="day">${window.moment(day.dt * 1000).format('ddd')}</div>
                <img src="http://openweathermap.org/img/wn/${day.weather[0].icon}@2x.png"
                alt="weather icon" class="w-icon">
                <div class="temp">Night - ${day.temp.night}&#176;C</div>
                <div class="temp">Day - ${day.temp.day}&#176;C</div>
            </div>`;
        }
    });

    weatherForecastEl.innerHTML = otherDayForcast;
}

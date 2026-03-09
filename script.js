const today = new Date();

for (let i = 1; i <= 5; i++) {
    const date = new Date();
    date.setDate(today.getDate() + i - 1);

    const dayName = date.toLocaleDateString("en-US", { weekday: "long" });
    const dayNumber = date.getDate();

    const column = document.getElementById("day" + i);

    column.querySelector(".day-name").textContent = dayName;

    if (i === 1) {
        column.querySelector(".date").textContent = "Today";
    } else if (i === 2) {
        column.querySelector(".date").textContent = "Tomorrow";
    }
     else {
        column.querySelector(".date").textContent = `${dayNumber}/${date.getMonth() + 1}`;
    }
}

const input = document.getElementById("time-input");
const dropdown = document.getElementById("time-dropdown");

for(let h=0; h<24; h++){

    const hour = h.toString().padStart(2,'0') + ":00";

    const option = document.createElement("div");
    option.className = "time-option";
    option.textContent = hour;

    option.addEventListener("click", () => {
        input.value = hour;
        dropdown.style.display = "none";
    });

    dropdown.appendChild(option);
}

dropdown.addEventListener("click", () =>{
    updateWeather();
})

input.addEventListener("click", () => {
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
});


// click outside
document.addEventListener("click", (e)=>{
    if(!e.target.closest(".time-picker")){
        dropdown.style.display = "none";
    }
});

window.addEventListener('pywebviewready', async function(){
    console.log("PyWebView ready!");
    updateWeather();
    
    const cities = await window.pywebview.api.get_available_cities();
    
    const datalist = document.getElementById('cities');
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        datalist.appendChild(option);
    });
});

window.addEventListener('pywebviewready', () => {
    const searchIcon = document.querySelector('.search-icon-abs');
    const cityInput = document.getElementById('city-input');


    searchIcon.addEventListener('click', async () => {
        updateWeather();
    });

    cityInput.addEventListener('keydown', async (event) => {
        if (event.key === "Enter")  {
            updateWeather();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const dayLinks = document.querySelectorAll('.day-link');
    const timeInput = document.getElementById('time-input');

    dayLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); 

            document.querySelectorAll('.day-column').forEach(column => {
                column.classList.remove('active');
            });

            const dayColumn = link.querySelector('.day-column');
            if (dayColumn) {
                dayColumn.classList.add('active');
                timeInput.value = "";
                updateWeather();
            }
        });
    });
});


async function updateWeather() {
        const cityInput = document.getElementById('city-input');
        const timeInput = document.getElementById('time-input');  
        const active = document.querySelector('.active').id;
        
        const today = new Date();
        let date = new Date();
        let time = "now";
        let city = "Timisoara";

        for (let i = 0; i <5; i++){
            if(active === 'day' + i){
                date.setDate(today.getDate() + i)
            }
        }

        date = date.toISOString().split('T')[0];

        if(timeInput.value !== ""){
            time = timeInput.value;
        }

        if(cityInput.value !== ""){
            city = cityInput.value;
        }

        const weatherInfo = await window.pywebview.api.get_weather_info(city, time, date);

        const temperatureElement = document.getElementById('temperature-now');
        temperatureElement.textContent = `${weatherInfo.temperature}°C`; 

        const cityNameElement = document.getElementById('city-name');
        city = city.charAt(0).toUpperCase() + city.slice(1);
        cityNameElement.textContent = city;

        timeInput.value = weatherInfo.time;
        
        const conditionElement = document.getElementById('condition');
        conditionElement.textContent = `${weatherInfo.condition.name}`;

        const mainEmojiElement = document.getElementById('main-emoji');
        mainEmojiElement.textContent = `${weatherInfo.condition.emoji}`;

        const windElement = document.getElementById('wind');
        windElement.textContent = `Wind: ${weatherInfo.wind} km/h`;

        const feelingElement = document.getElementById('feeling');
        feelingElement.textContent = `Feels like: ${weatherInfo.feeling} °C`;
}
// app.js
const citiesList = document.getElementById('cities-list');
const addCityBtn = document.getElementById('add-city-btn');

// Function to fetch all cities from backend
async function getCities() {
    try {
        const response = await axios.get('/cities');
        const cities = response.data;
        citiesList.innerHTML = '';
        cities.forEach(city => {
            const cityElement = document.createElement('div');
            cityElement.classList.add('city');
            cityElement.innerHTML = `
                <h3>${city.name}</h3>
                <p>Temperature: ${city.temperature} °C</p>
                <p>Humidity: ${city.humidity}%</p>
                <button onclick="deleteCity(${city.id})">Delete</button>
            `;
            citiesList.appendChild(cityElement);
        });
    } catch (error) {
        console.error('Error fetching cities:', error);
    }
}

// Function to delete a city
async function deleteCity(cityId) {
    try {
        await axios.delete(`/delete_city/${cityId}`);
        getCities();
    } catch (error) {
        console.error('Error deleting city:', error);
    }
}

// Event listener for add city button
addCityBtn.addEventListener('click', () => {
    const cityName = prompt('Enter city name:');
    if (cityName) {
        addCity(cityName);
    }
});

// Function to add a city
async function addCity(cityName) {
    try {
        await axios.post('/add_city', { city: cityName });
        getCities();
    } catch (error) {
        console.error('Error adding city:', error);
    }
}

// Initial fetch of cities
getCities();

from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    # Get city from POST or default to 'indore'
    city = request.POST.get('city', 'indore')

    # Weather API configuration
    WEATHER_API_KEY = '374cac6b6212edeeda1098ff3f258fe8'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

    # Google Search API configuration
    GOOGLE_API_KEY = 'AIzaSyAU_272RQJr-_eRZPhBSZEuHQm2atypaOY'
    SEARCH_ENGINE_ID = '71b0246c43c204876'

    # Default context in case of errors
    default_context = {
        'description': 'clear sky',
        'icon': '01d',
        'temp': 25,
        'day': datetime.date.today(),
        'city': city,
        'exception_occurred': True,
        'image_url': ''
    }

    try:
        # First try to get the weather data
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # This will raise an exception for 4XX/5XX status codes
        weather_data = weather_response.json()

        # Then try to get the city image
        image_query = f"{city} 1920x1080"
        city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={image_query}&searchType=image&imgSize=xlarge"

        image_response = requests.get(city_url)
        image_response.raise_for_status()
        image_data = image_response.json()

        # Get image URL with error handling
        search_items = image_data.get("items", [])
        image_url = search_items[0]['link'] if search_items else ''

        # If we got here, both API calls were successful
        return render(request, 'weatherapp/index.html', {
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
            'temp': weather_data['main']['temp'],
            'day': datetime.date.today(),
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        messages.error(request, f'Failed to fetch data: Network error')
        return render(request, 'weatherapp/index.html', default_context)

    except (KeyError, IndexError) as e:
        # Handle data parsing errors
        messages.error(request, 'Invalid data received from API')
        return render(request, 'weatherapp/index.html', default_context)

    except Exception as e:
        # Handle any other unexpected errors
        messages.error(request, 'An unexpected error occurred')
        return render(request, 'weatherapp/index.html', default_context)
import requests

def get_weather(city="Yaoundé"):
    """Récupère la météo en direct via l'API Open-Meteo (gratuite, sans clé API)."""
    try:
        # Geocoding pour obtenir les coordonnées de la ville
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=fr&format=json"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return f"Impossible de trouver la ville {city}."
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        
        # Obtention des données météo actuelles
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url).json()
        
        current = w_res.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")
        
        return f"À {city}, il fait actuellement {temp}°C avec un vent de {wind} km/h."
    except Exception as e:
        return f"Erreur lors de la récupération de la météo : {str(e)}"

def web_search(query):
    """Effectue une recherche rapide sur DuckDuckGo (sans clé API)."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        
        # Extraction simplifiée des résultats textuels
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        results = [a.get_text() for a in soup.find_all('a', class_='result__snippet')[:2]]
        
        if results:
            return " ".join(results)
        return "Aucun résultat précis trouvé sur le Web."
    except Exception as e:
        return f"Erreur lors de la recherche web : {str(e)}"
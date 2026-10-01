import os
import subprocess
import webbrowser
import requests
import pyttsx3
from bs4 import BeautifulSoup

def speak(self, text):
    """Synthèse vocale hors-ligne utilisant les voix SAPI5 de Windows."""
    def _speak_thread():
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)  # Vitesse de parole
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=_speak_thread, daemon=True).start()

def open_application(app_name):
    """Ouvre des applications système ou des sites web."""
    app_name = app_name.lower()
    
    if "navigateur" in app_name or "chrome" in app_name:
        webbrowser.open("https://www.google.com")
        return "Navigateur ouvert."
    elif "bloc-notes" in app_name or "notepad" in app_name:
        subprocess.Popen(["notepad.exe"])
        return "Bloc-notes ouvert."
    elif "calculatrice" in app_name:
        subprocess.Popen(["calc.exe"])
        return "Calculatrice lancée."
    elif "explorateur" in app_name or "fichiers" in app_name:
        subprocess.Popen(["explorer.exe"])
        return "Explorateur de fichiers ouvert."
    else:
        try:
            os.system(f"start {app_name}")
            return f"Ouverture de {app_name}."
        except Exception as e:
            return f"Erreur : {str(e)}"

def system_control(action):
    """Exécute des commandes système Windows."""
    action = action.lower()
    if "verrouiller" in action:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Session verrouillée."
    elif "extinction" in action or "éteindre" in action:
        os.system("shutdown /s /t 60")
        return "Extinction programmée dans 60 secondes."
    elif "annuler" in action:
        os.system("shutdown /a")
        return "Extinction annulée."
        
    return "Commande non reconnue."

def get_weather(city="Yaoundé"):
    """Récupère la météo actuelle via Open-Meteo."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=fr&format=json"
        geo_res = requests.get(geo_url, timeout=5).json()
        
        if not geo_res.get("results"):
            return f"Ville non trouvée : {city}."
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url, timeout=5).json()
        current = w_res.get("current_weather", {})
        
        return f"À {city}, il fait actuellement {current.get('temperature')}°C avec un vent de {current.get('windspeed')} km/h."
    except Exception as e:
        return f"Erreur météo : {str(e)}"

def web_search(query):
    """Recherche rapide sur DuckDuckGo."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = [a.get_text() for a in soup.find_all('a', class_='result__snippet')[:2]]
        
        if results:
            return " ".join(results)
        return "Aucun résultat trouvé sur le web."
    except Exception as e:
        return f"Erreur de recherche : {str(e)}"

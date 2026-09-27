import os
import subprocess
import webbrowser

def open_application(app_name):
    """Ouvre des applications système ou des logiciels courants."""
    app_name = app_name.lower()
    
    if "navigateur" in app_name or "chrome" in app_name:
        webbrowser.open("https://www.google.com")
        return "J'ai ouvert le navigateur."
        
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
        # Essayer de lancer directement la commande via le terminal Windows
        try:
            os.system(f"start {app_name}")
            return f"Tentative d'ouverture de {app_name} effectuée."
        except Exception as e:
            return f"Impossible d'ouvrir {app_name} : {str(e)}"

def system_control(action):
    """Gère des commandes système de base."""
    action = action.lower()
    
    if "verrouiller" in action:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Session verrouillée."
        
    elif "extinction" in action or "éteindre" in action:
        # Extinction programmée dans 60 secondes pour sécurité (annulable via 'shutdown -a')
        os.system("shutdown /s /t 60")
        return "Extinction du système programmée dans 60 secondes."
        
    elif "annuler extinction" in action:
        os.system("shutdown /a")
        return "Extinction annulée."
        
    return "Commande système non reconnue."

import tools

def execute_tool(action, target):
    """Routeur pour exécuter les outils externes."""
    if action == "get_weather":
        return tools.get_weather(target if target else "Yaoundé")
    elif action == "web_search":
        return tools.web_search(target)
    return None
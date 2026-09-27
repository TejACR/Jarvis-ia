import sounddevice as sd
import numpy as np
import asyncio
import edge_tts
import pygame
import ollama
import os
from openwakeword.model import Model

import json
import actions  # Importation du fichier actions.py créé ci-dessus

# System prompt enrichi pour la détection d'intentions
SYSTEM_PROMPT = """Tu es Jarvis, un assistant IA exécuté sur un PC Windows.
Tu peux exécuter des actions système si l'utilisateur le demande.

Si l'utilisateur demande une action sur le PC, réponds STRICTEMENT sous forme de JSON valide avec cette structure :
{"action": "open_app", "target": "nom_de_l_application"}
OU
{"action": "system_control", "target": "verrouiller/éteindre/annuler extinction"}

Si c'est une question générale ou une discussion, réponds simplement avec une phrase courte et concise (2 phrases max).
Ne rajoute aucun texte autour du JSON si tu choisis d'exécuter une action.
Tu as accès à des outils externes pour répondre aux besoins de l'utilisateur.

Si la demande nécessite une action système ou une recherche externe, réponds STRICTEMENT avec ce JSON :
- Météo : {"action": "get_weather", "target": "NomDeLaVille"}
- Recherche Web : {"action": "web_search", "target": "mots clés de recherche"}
- Application : {"action": "open_app", "target": "nom_app"}

Exemples :
Utilisateur : "Quelle est la météo à Douala ?" -> {"action": "get_weather", "target": "Douala"}
Utilisateur : "Qui a gagné le dernier match de football ?" -> {"action": "web_search", "target": "dernier match resultat football"}

Si aucune action n'est requise, réponds directement en texte concis (2 phrases max)
"""


def process_command(user_input):
    """Analyse la commande, exécute l'action si nécessaire ou génère une réponse."""
    raw_response = ask_llm(user_input).strip()
    
    # Vérification si le LLM demande une exécution d'action via JSON
    if raw_response.startswith("{") and raw_response.endswith("}"):
        try:
            cmd = json.loads(raw_response)
            action_type = cmd.get("action")
            target = cmd.get("target")
            
            if action_type == "open_app":
                result = actions.open_application(target)
                return result
            elif action_type == "system_control":
                result = actions.system_control(target)
                return result
        except json.JSONDecodeError:
            pass  # En cas d'erreur de parsing JSON, traiter comme une réponse texte
            
    return raw_response

# --- CONFIGURATION ---
WAKEWORD_NAME = "hey_jarvis"
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # Taille de bloc requise par openWakeWord

SYSTEM_PROMPT = """Tu es Jarvis, un assistant IA très intelligent, rapide et courtois. 
Tes réponses doivent être concises (2 à 3 phrases maximum) pour être lues facilement à voix haute."""

# Initialisation du modèle de veille openWakeWord
oww_model = Model(wakeword_models=[WAKEWORD_NAME], inference_framework="onnx")

async def speak(text):
    """Génère la voix avec Edge-TTS et la joue avec Pygame."""
    output_file = "response.mp3"
    communicate = edge_tts.Communicate(text, voice="fr-FR-RemyNeural")
    await communicate.save(output_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    if os.path.exists(output_file):
        os.remove(output_file)

def ask_llm(prompt):
    """Envoie la consigne à Ollama (Llama 3.2 ou Mistral)."""
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': prompt},
    ])
    return response['message']['content']

async def main():
    print("--- Jarvis est en ligne et en veille ---")
    await speak("Système Jarvis initialisé. En attente du mot clé.")
    
    def audio_callback(indata, frames, time, status):
        """Callback appelé à chaque bloc d'enregistrement audio."""
        if status:
            print(status)
        # Normalisation des données audio pour openWakeWord
        audio_data = (indata[:, 0] * 32767).astype(np.int16)
        prediction = oww_model.predict(audio_data)
        
        if prediction[WAKEWORD_NAME] > 0.5:
            print("\n[!] Mot-clé détecté ! Jarvis réactivé.")
            oww_model.reset()
            raise sd.CallbackStop

    while True:
        print("\n[Veille] Écoute du mot-clé 'Hey Jarvis'...")
        try:
            # Écoute en continu via sounddevice
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback, blocksize=CHUNK_SIZE):
                while True:
                    await asyncio.sleep(0.1)
        except sd.CallbackStop:
            # Le mot clé a été détecté
            await speak("Oui ? Je vous écoute.")
            
            # Ici, vous pouvez saisir une commande texte ou connecter la transcription vocale
            user_query = input("Votre commande (ou appuyez sur Entrée) : ")
            
            if user_query.strip():
                if "stop" in user_query.lower():
                    await speak("Mise en veille du système.")
                    break
                
                print("Jarvis réfléchit...")
                reply = ask_llm(user_query)
                print(f"Jarvis : {reply}")
                await speak(reply)

if __name__ == "__main__":
    asyncio.run(main())
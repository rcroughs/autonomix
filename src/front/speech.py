from speech_recognition import Recognizer, Microphone
from g4f.client import Client
import datetime

recognizer = Recognizer()


with Microphone() as source:
    print("Réglage du bruit ambiant... Patientez...")
    recognizer.adjust_for_ambient_noise(source)
    print("Vous pouvez parler...")
    recorded_audio = recognizer.listen(source)
    print("Enregistrement terminé !")

try:
    print("Reconnaissance du texte...")
    text = recognizer.recognize_vosk(recorded_audio, language="fr-FR")
    print("Texte reconnu: " + text)
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "Assistant",
                "content": f"Traducteur entre un texte générée depuis de Speech-to-Text vers un format ISO8601. Nous sommes actuellement le {datetime.datetime.now().isoformat()}. Ne donner uniquement la réponse: "
                + text,
            }
        ],
    )
    print(response.choices[0].message.content)
except Exception as ex:
    print(ex)

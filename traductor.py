import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
puntaje = 0
vida = 3
rondas = 1 
#diccionario
words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}


idioma = input("Ingrese el idioma en el cual hablará (es - en):")
#pregunta la dificultad
dificultad = input("Ingrese la dificultad:")

while vida > 0 and rondas <= 3:
    print("--- RONDA", rondas, "de 3 ---")

    #escoger la palabra segun la dificultad ducha por el usuario
    palabra = random.choice(words_by_level[dificultad])
    print("Jugador, la palabra que debe traducir es:", palabra)

    duration = 5  # segundos de grabación
    sample_rate = 44100
    print("Habla ahora...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, reconociendo...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language= idioma).lower()
        print("Dijiste:", text)
        traduccion = GoogleTranslator(source="auto", targe="en").translate(palabra)
    
        if text.lower() == traduccion.lower():
            print("¡Lo hiciste increíble✅🤩!")
            puntaje += 1
            print("Tu puntaje es:", puntaje)
        else:
            print("¡Casi lo logras! Pasamos a la siguiente ronda❌😔")
            vida -= 1
            print("Te quedan", vida, "vidas")
            
        
        
        print("La traduccion de la palabra es:", traduccion)
        
    except sr.UnknownValueError:
        print("No se pudo reconocer el habla. Perdiste una vida por intento fallido.")
        vida -= 1
        print("Te quedan", vida, "vidas")
    except sr.RequestError as e:
        print(f"Error del servicio: {e}")

    rondas += 1

# Evaluación final del juego
print("--- JUEGO TERMINADO ---")
if vida == 0:
    print("Te has quedado sin vidas. ¡Mejor suerte la próxima vez!")
else:
    print("¡Felicidades por completar las 3 rondas! Tu puntaje final es:", puntaje)



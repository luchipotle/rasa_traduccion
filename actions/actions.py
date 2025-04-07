from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import List, Dict, Text, Any
import random
from googletrans import Translator


class ActionSetDetectedLanguage(Action):
    def name(self) -> Text:
        return "action_set_detected_language"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Obtener el valor del idioma detectado
        # Suponiendo que el componente agregó la información en la metadata del mensaje
        last_message = tracker.latest_message
        detected_language = last_message.get("detected_language")

        if not detected_language:
            detected_language = "es"  # Valor por defecto si no se detectó nada

        # Opcional: Puedes enviar un mensaje de log o debug
        dispatcher.utter_message(text=f"Idioma detectado: {detected_language}")

        return [SlotSet("detected_language", detected_language)]


class ActionPreguntarNombre(Action):
    def name(self) -> Text:
        return "action_preguntar_nombre"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:

        # Mensaje base en español
        es_text = "¡Hola! ¿Cómo te llamas? 🙂"

        # Obtenemos el idioma detectado del slot (o 'es' por defecto)
        detected_language = tracker.get_slot("detected_language") or "es"

        # Si el idioma no es español, traducimos
        if detected_language != "es":
            try:
                translator = Translator()
                translated_text = translator.translate(es_text, dest=detected_language).text
                es_text = translated_text
            except Exception as e:
                # Si falla, mantenemos el español
                pass

        dispatcher.utter_message(text=es_text)
        return []


class ContarCuriosidad(Action):
    def name(self) -> Text:
        return "action_contar_curiosidad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lista de curiosidades en español
        respuestas = [
            "¿Sabías que la miel nunca se echa a perder? Se han encontrado vasijas de miel en tumbas egipcias que aún eran comestibles.",
            "El corazón de una ballena azul es tan grande que un humano podría nadar a través de sus arterias.",
            "Los pulpos tienen tres corazones y la sangre azul.",
            "Las abejas pueden reconocer rostros humanos.",
            "Australia es más ancha que la Luna. La Luna tiene 3400 km de diámetro, mientras que el diámetro de Australia de este a oeste es de casi 4000 km.",
            "En Suiza es ilegal tener una sola cobaya. Se considera maltrato animal porque son seres sociales y se sienten solos."
        ]

        # Elegimos una curiosidad al azar
        respuesta_es = random.choice(respuestas)

        # Obtenemos el idioma detectado
        detected_language = tracker.get_slot("detected_language") or "es"

        # Si no es español, traducimos la curiosidad
        if detected_language != "es":
            try:
                translator = Translator()
                respuesta_traducida = translator.translate(respuesta_es, dest=detected_language).text
                respuesta_es = respuesta_traducida
            except Exception as e:
                pass

        dispatcher.utter_message(text=respuesta_es)
        return []


class ActionSaludoPersonalizado(Action):
    def name(self) -> Text:
        return "action_saludo_personalizado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nombre = tracker.get_slot("nombre_usuario") or "amigo"
        texto_es = f"¡Genial, {nombre}! ¿Qué quieres hacer?"

        detected_language = tracker.get_slot("detected_language") or "es"

        if detected_language != "es":
            try:
                translator = Translator()
                texto_traducido = translator.translate(texto_es, dest=detected_language).text
                texto_es = texto_traducido
            except Exception as e:
                pass

        dispatcher.utter_message(text=texto_es)
        return []
    

class ActionResponderAgradecimiento(Action):
    def name(self) -> Text:
        return "action_responder_agradecimiento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        texto_es = "Gracias a ti, ¿quieres otro dato curioso? 😃"

        detected_language = tracker.get_slot("detected_language") or "es"

        if detected_language != "es":
            try:
                translator = Translator()
                texto_traducido = translator.translate(texto_es, dest=detected_language).text
                texto_es = texto_traducido
            except Exception as e:
                pass

        dispatcher.utter_message(text=texto_es)
        return []
    
class ActionDespedida(Action):
    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nombre = tracker.get_slot("nombre_usuario") or "amigo"
        texto_es = f"¡Hasta pronto, {nombre}!"

        detected_language = tracker.get_slot("detected_language") or "es"

        if detected_language != "es":
            try:
                translator = Translator()
                texto_traducido = translator.translate(texto_es, dest=detected_language).text
                texto_es = texto_traducido
            except Exception as e:
                pass

        dispatcher.utter_message(text=texto_es)
        return []


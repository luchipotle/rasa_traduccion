from __future__ import annotations
from typing import List, Dict, Text, Any
import logging

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

# fasttext para detección y googletrans para traducción
import fasttext
from googletrans import Translator

logger = logging.getLogger(__name__)

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)
class LanguageDetectionComponent(GraphComponent):
    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
        model_storage: ModelStorage,
        resource: Resource,
    ) -> None:
        self.config = config
        self.name = name
        self._model_storage = model_storage
        self._resource = resource

        # Cargar el modelo FastText. La ruta se puede definir en el config.
        model_path = config.get("fasttext_model_path", "lid.176.ftz")
        try:
            self.language_model = fasttext.load_model(model_path)
        except Exception as e:
            logger.error(f"No se pudo cargar el modelo FastText desde {model_path}: {e}")
            raise e

        # Inicializamos el traductor
        self.translator = Translator()

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, execution_context.node_name, model_storage, resource)

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            original_text = message.get("text")
            if not original_text:
                continue

            try:
                # Detectar el idioma con FastText
                predictions = self.language_model.predict(original_text)
                # fastText devuelve una etiqueta como "__label__en", extraemos el código de idioma
                detected_language = predictions[0][0].replace("__label__", "")
            except Exception as e:
                logger.error(f"Error al detectar idioma con FastText: {e}")
                detected_language = "es"  # Valor por defecto

            # Guardamos el idioma detectado en la metadata del mensaje
            message.set("detected_language", detected_language)

        # Añadir entidad al mensaje
            entities = message.get("entities", [])
            entities.append(
                {
                    "entity": "detected_language",
                    "value": detected_language,
                    "confidence": 1.0,
                    "start": 0,
                    "end": 0,
                    "extractor": "LanguageDetectionComponent",
                }
            )
            message.set("entities", entities)

            # Si el idioma no es español, traducimos el texto al español
            if detected_language != "es":
                try:
                    translated = self.translator.translate(original_text, dest="es")
                    message.set("text", translated.text)
                except Exception as e:
                    logger.error(f"Error al traducir al español: {e}")
                    # Si falla la traducción, se mantiene el texto original

        return messages

    def persist(self) -> None:
        # En este ejemplo, no es necesario persistir nada.
        pass

    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, execution_context.node_name, model_storage, resource)

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # No se modifica la data de entrenamiento en este componente
        return training_data

    @staticmethod
    def required_packages() -> List[Text]:
        # Declaramos las dependencias necesarias para este componente.
        return ["fasttext", "googletrans"]

import requests
import json

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

from .integrations import Integrations

class ActionInformacionPokemon(Action):

    def name(self) -> Text:
        return "action_informacion_pokemon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pokemon_name = tracker.get_slot('pokemon_name')

        integracion = Integrations()
        
        request_informacion_pokemon = integracion.pokemon_information(pokemon_name=pokemon_name)

        abilities_num = request_informacion_pokemon.get('abilities_num')
        pokemon_abilities = request_informacion_pokemon.get('abilities')
        pokemon_type = request_informacion_pokemon.get('type')
        error = request_informacion_pokemon.get('error')

        if error=="":
            return [SlotSet('abilities_num', abilities_num), 
            SlotSet('pokemon_abilities', pokemon_abilities), 
            SlotSet('pokemon_type', pokemon_type)]
        else:
            dispatcher.utter_message('ERROR: El servicio de información pokémon no responde correctamente o no se encuentra información para ese nombre. Por favor, intenta más tarde o prueba otro nombre.')
            return [FollowupAction('utter_reingreso_menu')]

class ActionMostrarEntidades(Action):

    def name(self) -> Text:
        return "action_mostrar_entidades"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message_entities = tracker.latest_message.get('entities')

        print(latest_message_entities)
        dispatcher.utter_message(str(latest_message_entities))
        return []

class ValidateUserNameForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_user_name_form"
    
    async def extract_user_name(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
        ) -> Dict[Text, Any]:

        counter = tracker.get_slot('counter')

        if counter==0:
            print('COUNTER: ', counter)
            print('...ASKING NAME...')
            return {'user_name': None}
        else:
            print('COUNTER != 0')
            latest_entities_array = tracker.latest_message.get('entities')
            print('LATEST_ENTITIES_ARRAY: ',latest_entities_array)
            if len(latest_entities_array)>=1:
                user_name_list = []
                for i in latest_entities_array:
                    entity_type = i['entity']
                    print('LATEST_ENTITY_TYPE: ', entity_type)
                    entity_value = i['value']
                    print('LATEST_ENTITY_VALUE: ',entity_value)
                    entity_extractor = i['extractor']
                    print('LATEST_ENTITY_EXTRACTOR: ', entity_extractor)
                    if entity_type=='PER' and entity_extractor=='SpacyEntityExtractor':
                        user_name_list.append(entity_value)
                if len(user_name_list)==1:
                    return {'user_name': str(user_name_list[0]).capitalize()}
                elif len(user_name_list)>=2:
                    complete_user_name = ''
                    for i in user_name_list:
                        i = str(i).capitalize()
                        complete_user_name += i
                    return {'user_name': complete_user_name}
                else:
                        print('NOT NAME VALUE RECEIVED - NONE')
                        return {'user_name': None}
            else:
                print('NO ENTITIES RECEIVED - NONE')
                return {'user_name': None}

    def validate_user_name(        
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
            ) -> Dict[Text,Any]:

            counter = tracker.get_slot('counter')

            if slot_value is not None:
                print('...SLOT VALUE VALIDATED...')
                return {'user_name': slot_value, 'counter': 0}
            else:
                counter += 1
                print('COUNTER: ', counter)
                if counter>1:
                    dispatcher.utter_message('No pude reconocer tu nombre, por favor, inténtalo de nuevo')
                return {'user_name': None, 'counter': counter}

class ValidatePokemonNameForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_pokemon_name_form"
    
    async def extract_pokemon_name(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
        ) -> Dict[Text, Any]:

        counter = tracker.get_slot('counter')
        print('COUNTER: ', counter)

        if counter==0:
            print('...COUNTER=0...')
            return {'pokemon_name': None, counter: 0}
        else:
            print('...COUNTER!=0...')
            latest_entities_array = tracker.latest_message.get('entities')
            print('LATEST_ENTITIES_ARRAY: ', latest_entities_array)
            if len(latest_entities_array)>=1:
                pokemon_name_list = []
                for i in latest_entities_array:
                    print('ARRAY ELEMENT: ',i)
                    entity_type = i['entity']
                    print('ENTITY_TYPE: ', entity_type)
                    entity_extractor = i['extractor']
                    print('EXTRACTOR: ', entity_extractor)
                    if entity_type=='pokemon_name' and entity_extractor=="DIETClassifier":
                        pokemon_name_list.append(i['value'])
                    print('LATEST_ENTITY_VALUES: ', pokemon_name_list)
                if len(pokemon_name_list)>=1:
                    print('...POKEMON NAME...')
                    return {'pokemon_name': str(pokemon_name_list[0]).lower()}
                else:
                    print('NOT POKEMON NAME ENTITY - NONE')
                    return {'pokemon_name': None}
            else:
                print('NO ENTITIES - NONE')
                return {'pokemon_name': None}

    def validate_pokemon_name(        
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
            ) -> Dict[Text,Any]:

            counter = tracker.get_slot('counter')

            if slot_value is not None:
                print('...SLOT VALUE...')
                return {'pokemon_name': slot_value, 'counter': 0}
            else:
                print('INVALID SLOT VALUE')
                counter += 1
                if counter>1:
                    dispatcher.utter_message('No pude reconocer el nombre del pokemon que estás buscando, por favor, inténtalo de nuevo')
                return {'pokemon_name': None, 'counter': counter}
import requests
import json

POKEMON_ENDPOINT = "https://pokeapi.co/api/v2/pokemon"

class Integrations():

    def pokemon_information(self, pokemon_name) -> dict:
        
        self.pokemon_information_dict = {
            "abilities_num": "",
            "abilities": "",
            "type": "",
            "error": ""
        }

        try:

            response = requests.get(url=f'{POKEMON_ENDPOINT}/{pokemon_name}').json()

            pokemon_type = ""
            types_len = len(response['types'])
            print('LEN TYPES: ',types_len)
            if types_len==1:
                pokemon_type += f"es de tipo {response['types'][0]['type']['name']}."
            else:
                for index, item in enumerate(response['types']):
                    if index==0:
                        pokemon_type += f"es de los tipos: {item['type']['name']}"
                    elif index==types_len-1:
                        pokemon_type += f" y {item['type']['name']}."
                    elif index<types_len:
                        pokemon_type += f", {item['type']['name']}"
            
            print('POKEMON TYPE: ', pokemon_type)

            pokemon_abilities = ""
            abilities_len = len(response['abilities'])
            print('ABILITIES_LEN: ', abilities_len)
            if abilities_len==1:
                pokemon_abilities += f"{response['abilities'][0]['ability']['name']}."
            else:
                for index, item in enumerate(response['abilities']):
                    print('INDEX ABILITIES: ', index)
                    if index==0:
                        pokemon_abilities += f"{item['ability']['name']}"
                    elif index==abilities_len-1:
                        pokemon_abilities += f" y {item['ability']['name']}."
                    elif index<abilities_len:
                        pokemon_abilities += f", {item['ability']['name']}"

            print('POKEMON ABILITIES: ', pokemon_abilities)
            
            abilities_len_str = f"Tiene 1 habilidad" if abilities_len==1 else f"Tiene {str(abilities_len)} habilidades"

            print('POKEMON ABILITIES NUMBER: ', abilities_len_str)

            self.pokemon_information_dict['abilities_num'] = str(abilities_len_str)
            self.pokemon_information_dict['abilities'] = pokemon_abilities
            self.pokemon_information_dict['type'] = pokemon_type
            
        except Exception as e:
            self.pokemon_information_dict['error'] = str(e)
            print('[ERROR] ',str(e))
        
        return self.pokemon_information_dict


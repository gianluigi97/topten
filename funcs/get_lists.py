from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(r"C:\GianC\topten\key.env")

class ListTen:

    def __init__(self):

        self._client = None
        self._key = os.getenv("api_key")

    def _get_client(self):

        if self._client: 
            return self._client

        self._client = OpenAI(api_key=self._key)
        return self._client
        

    def get_rank(self, *, model="gpt-5.6-luna", richiesta):

        client = self._get_client()

        response = client.responses.create(
            model=model,
            input=f"""
            Stilami una classifica dei/delle top 10: {richiesta}

            Restituisci esattamente 10 risultati,
            ordinati dal primo al decimo.
            """,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "top_10",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "classifica": {
                                "type": "array",
                                "minItems": 10,
                                "maxItems": 10,
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "posizione": {
                                            "type": "integer"
                                        },
                                        "nome": {
                                            "type": "string"
                                        },
                                        "descrizione": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "posizione",
                                        "nome",
                                        "descrizione"
                                    ],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["classifica"],
                        "additionalProperties": False
                    }
                }
            }
        )

        return json.loads(response.output_text)



    def format_ia_response(self, response, categoria=None, db=False):

        if not db:
            return [
                {"nome": el.get("nome")}
                for el in response["classifica"]
            ]

        return [
            {
                "posizione": el.get("posizione"),
                "nome": el.get("nome"),
                "famiglia": categoria
            }
            for el in response["classifica"]
    ]


if __name__ == "__main__":

    lt = ListTen()
    response = lt.get_rank(richiesta="nomi femminili più usati in italia")

    for el in response['classifica']:
        print(el)
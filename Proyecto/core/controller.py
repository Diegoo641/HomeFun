import mercadopago
class Controller:
    def pagar(self,total):
        # Agrega credenciales
        sdk = mercadopago.SDK("TEST-8089418270941450-052521-0d2b104ed9c05b1dd8dbdd973340f776-1381512793")

        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "aireAcondionado",
                    "quantity": 1,
                    "unit_price": int(total)
                },

            ],
                "back_urls": {
                            "success": "http://127.0.0.1:8000/productos",
                            "failure": "http://127.0.0.1:8000/productos",
                            "pending": "http://127.0.0.1:8000/productos"
                            },
                "auto_return": "approved"

        }
        
        preference_response = sdk.preference().create(preference_data)
        #preference = preference_response["response"]
        return preference_response

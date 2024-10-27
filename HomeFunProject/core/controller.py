
# SDK de Mercado Pago
import mercadopago



class Controller:
    
    def pagar():
        # Agrega credenciales
        sdk = mercadopago.SDK("TEST-3511773968506450-102717-8677de7085489db9d366c7d4281a0e4a-255638280")

        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "Miproducto",
                    "quantity": 1,
                    "unit_price": 100
                },

            ],
                "back_urls": {
                            "success": "http://127.0.0.1:8000/pagarDeuda",
                            "failure": "http://127.0.0.1:8000/pagarDeuda",
                            "pending": "http://127.0.0.1:8000/pagarDeuda"
                            },
                "auto_return": "approved"

        }
        
        preference_response = sdk.preference().create(preference_data)
        #preference = preference_response["response"]
        return preference_response


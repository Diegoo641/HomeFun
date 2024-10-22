
# SDK de Mercado Pago
import mercadopago



class Controller:
    
    def pagar():
        # Agrega credenciales
        sdk = mercadopago.SDK("")

        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "aireAcondionado",
                    "quantity": 1,
                    "unit_price": 100
                },

            ],
                "back_urls": {
                            "success": "http://127.0.0.1:8000/consulta_estado_cuenta",
                            "failure": "http://127.0.0.1:8000/consulta_estado_cuenta",
                            "pending": "http://127.0.0.1:8000/consulta_estado_cuenta"
                            },
                "auto_return": "approved"

        }
        
        preference_response = sdk.preference().create(preference_data)
        #preference = preference_response["response"]
        return preference_response


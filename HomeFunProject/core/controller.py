
# SDK de Mercado Pago
import mercadopago



class Controller:
    
    def pagar(self,total):
        # Agrega credenciales
        sdk = mercadopago.SDK("")

        # Crea un ítem en la preferencia
        preference_data = {
      # the "purpose": "wallet_purchase", allows only logged in payments
      # to allow guest payments, you can omit this property
            "purpose": "wallet_purchase",
            "items":[{
                    "title": "My Item",
                    "quantity": 1,
                    "unit_price": total  
                }]
                }
        
        preference_response = sdk.preference().create(preference_data)
        #preference = preference_response["response"]
        return preference_response


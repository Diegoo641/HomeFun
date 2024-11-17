
# SDK de Mercado Pago
import mercadopago



class Controller:
    
    def pagar(self):
        # Agrega credenciales
        sdk = mercadopago.SDK("TEST-799766335101209-102200-dc91acd07d20881aa5b98b60bf6e8129-2049276181")

        # Crea un ítem en la preferencia
        preference_data = {
      # the "purpose": "wallet_purchase", allows only logged in payments
      # to allow guest payments, you can omit this property
            "purpose": "wallet_purchase",
            "items":[{
                    "title": "My Item",
                    "quantity": 1,
                    "unit_price": 75.56  
                }]
                }
        
        preference_response = sdk.preference().create(preference_data)
        #preference = preference_response["response"]
        return preference_response


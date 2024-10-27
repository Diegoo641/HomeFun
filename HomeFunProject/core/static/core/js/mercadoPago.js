const mp = new MercadoPago('YOUR_PUBLIC_KEY',{
    locale: "es-AR",
});

document.getElementById("checkout-btn").addEventListener("click", async ()=> {
    try{    const orderData = {
        title: "Prueba",
        quanty : 1,
        price: 100,
    };

    const response = await fetch ("http://127.0.0.1:8000/create_preference",{
        method: "POST",
        headers: {
            "Content-Type": "application/json",

        },
        body: JSON.stringify(orderData),
    });

    const preference = await response.json();
    creatCheckoutButton(preference.id);
} catch (error) {
    alert("error :(");
}
});

const creatCheckoutButton = (preferenceId) => {
    const bricksBuilder = mp.bricks();

    const renderComponent = async () =>{
        if (window.checkoutButton) window.checkoutButton.unmount();
        bricksBuilder.create("wallet", "wallet_container", {
            initialization: {
                preferenceId: preferenceId,
            },
         customization: {
          texts: {
           valueProp: 'smart_option',
          },
          },
         });
         
    }



    renderComponent();
};
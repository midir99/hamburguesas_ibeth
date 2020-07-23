let app = new Vue({
    el: '#content',
    delimiters: ['[[', ']]'],
    data: {
        message: "Hi, I'm a message",
        cart: "[]",
        categoryIngredients: {
            Hamburguesa: ['Chile', 'Cebolla', 'Catsup', 'Mostaza', 'Piña'],
            Torta: ['Chile', 'Queso Oaxaca'],
            Bebida: ['Chispas de Chocolate', 'Crema batida', 'Escarchado de chocolate'],
            Postre: ['Crema batida'],
        },
        orderModalData: {},
    },
    methods: {
        sayHello() {
            console.log(this.message);
        },
        addToCart() {
            let name = document.getElementById('modalDishTitle').innerText;
            let price = Number(document.getElementById('modalDishPrice').innerText.slice(1));
            let quantity = Number(document.getElementById('modalQuantity').value);
            let modalIngredientsCheckBoxList = document.getElementById('modalIngredientsCheckBoxList');
            let imgUrl = document.getElementById('modalDishImg').src || '';
            let ingredients = [];
            for (let node of modalIngredientsCheckBoxList.childNodes) {
                let inp = node.childNodes[0];
                if (inp.checked) {
                    ingredients.push(inp.name);
                }
            }

            let newCart = JSON.parse(this.cart);
            newCart.push({ name, price, ingredients, imgUrl, quantity, id: 'dish' + Math.random().toString(36).substring(2) });
            this.cart = JSON.stringify(newCart);
        },
        configureOrderModal(name, category, price, imgUrl) {

            let ingredients = {
                'Hamburguesa': ['Chile', 'Cebolla', 'Jitomate'],
                'Torta': ['Chile', 'Queso Oaxaca'],
                'Bebida': ['Chispas de Chocolate', 'Crema batida', 'Escarchado de chocolate'],
                'Postre': ['Crema batida'],
            };

            document.getElementById('modalDishTitle').innerText = name;
            document.getElementById('modalDishPrice').innerText = `$${price}`;
            document.getElementById('modalDishImg').src = imgUrl;
            document.getElementById('modalQuantity').value = 1;

            let modalIngredientsCheckBoxList = document.getElementById('modalIngredientsCheckBoxList');
            modalIngredientsCheckBoxList.innerHTML = '';
            for (let ing of ingredients[category]) {
                let li = document.createElement("li");
                li.innerHTML = `<input type="checkbox" checked name="${ing}"> ${ing}`;
                modalIngredientsCheckBoxList.appendChild(li);
            }
        },
        addToCartAndGoCheckOut() {
            console.log('Going to checkout');
            this.addToCart();
            location.href = '/cart/';
        },
        removeListDish(id) {
            let newCart = JSON.parse(this.cart);
            newCart = newCart.filter(e => e.id !== id);
            this.cart = JSON.stringify(newCart);
            let cr = document.getElementById(id);
            // console.log(`Hola ${id}`);
            // console.log(cr);
            // cr.parentNode.removeChild(cr);
        },
        sendWaMessage() {
            let cart = JSON.parse(this.cart);
            let message = `Hola, me gustaría ordenar\n\n`;
            let total = 0;
            for (let dish of cart) {
                message += `=> ${dish.quantity} ${dish.name} con:\n`;
                for (let ing of dish.ingredients) {
                    message += `   • ${ing}\n`;
                }
                message += `\n   $ ${dish.price} c/u * ${dish.quantity} = $ ${dish.quantity * dish.price}\n\n`;
                total += dish.quantity * dish.price;
            }
            message += `Por todo serían ${total} pesos.\n¿A que hora podría traerme mi pedido?`
            // console.log(message);
            message = window.encodeURI(message);
            // console.log(message);
            this.cart = "";
            location.href = `https://wa.me/5217772326156?text=${message}`
        }
    },
    computed: {
        shoppingCart() {
            return JSON.parse(this.cart);
        },
        getTotalCost() {
            let currentCart = JSON.parse(this.cart);
            let total = 0;
            for (let dish of currentCart) {
                total += dish.price * dish.quantity;
            }
            return total;
        }
    },
    mounted() {
        if (localStorage.cart) {
              this.cart = localStorage.cart;
              this.shoppingCartData = JSON.parse(this.cart);
        }
    },
    watch: {
        cart(newVal) {
            localStorage.cart = newVal;
        }
    }
});
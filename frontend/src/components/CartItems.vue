<template>
    <div class="cart-container">
        <h2>Cart</h2>
        <ul class="cart-list">
            <li v-for="(item, productId) in cartCopy" :key="productId" class="cart-item">
                {{ item.productName }} - Quantity: {{ item.quantity }}
                <button @click="incrementQuantity(productId)" class="action-button">+</button>
                <button @click="decrementQuantity(productId)" class="action-button">-</button>
                <button @click="removeFromCart(productId)" class="action-button">Remove</button>
            </li>
        </ul>
        <p class="total">Total: {{ calculateTotal }}</p>
        <button @click="buyItems" class="buy-button">Buy Items</button>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        cart: Object, // cart is a prop
    },
    data() {
        return {
            cartCopy: {}, // Create a local copy of the cart
        };
    },
    computed: {
        calculateTotal() {
            // Calculate the total price based on the local cart copy
            return Object.values(this.cartCopy).reduce((total, item) => {
                return total + item.quantity * item.price;
            }, 0);
        },
    },
    methods: {
        incrementQuantity(productId) {
            // Modify the local cart copy
            if (this.cartCopy[productId].quantity < this.cartCopy[productId].available) {
                this.cartCopy[productId].quantity++;
                this.updateParentCart(this.cartCopy);
            }
            console.log(this.cartCopy[productId].available);
        },
        decrementQuantity(productId) {
            // Modify the local cart copy
            if (this.cartCopy[productId].quantity > 1) {
                this.cartCopy[productId].quantity--;
                this.updateParentCart(this.cartCopy);
            }
        },
        removeFromCart(productId) {
            // Remove the item from the local cart copy
            delete this.cartCopy[productId];
            this.updateParentCart(this.cartCopy);
        },
        buyItems() {
            const itemsToBuy = Object.values(this.cart).map(item => ({
                product_id: item.id,
                quantity: item.quantity,
                productName: item.productName,
                price: item.price,
            }));
            const accessToken = localStorage.getItem('access_token');
            axios.post('/buy-items', { items: itemsToBuy }, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            })
                .then(response => {
                    console.log(response.data); 
                    this.cartCopy = {};// Output success message or do something else
                    // Clear the cart or update the view accordingly
                })
                .catch(error => {
                    console.error('Error buying items:', error);
                });
        },
        updateParentCart(cartCopy) { 
            this.$emit('updateCart', cartCopy);
        },
    },
    created() {
        // Create the local cart copy
        this.cartCopy = { ...this.cart };
    },
};
</script>

<style scoped>
.cart-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.cart-list {
    list-style: none;
    padding: 0;
}

.cart-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 5px;
}

.action-button {
    background-color: #3498db;
    color: white;
    padding: 5px 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-left: 5px;
}

.action-button:hover {
    background-color: #2980b9;
}

.total {
    margin-top: 10px;
    font-weight: bold;
}

.buy-button {
    background-color: #2ecc71;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-top: 10px;
}

.buy-button:hover {
    background-color: #27ae60;
}
</style>



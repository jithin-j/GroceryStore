<template>
    <div class="dashboard-container">
        <button @click="logout" class="logout-button">Logout</button>
        <h2>User Dashboard</h2>
        <div class="filter-section">
            <label for="sectionFilter">Filter by Section:</label>
            <select id="sectionFilter" v-model="filter.sectionId" class="filter-select">
                <option value="All">All</option>
                <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
            </select>
        </div>
        <div class="filter-section">
            <label for="priceFilter">Filter by Max Price:</label>
            <input type="number" id="priceFilter" v-model="filter.maxPrice" class="filter-input">
        </div>
        <div class="filter-section">
            <label for="productSearch">Search for Product:</label>
            <input type="text" id="productSearch" v-model="searchProduct" @input="performSearch" class="filter-input">
        </div>
        <div v-for="section in sections" :key="section.id" class="product-section">
            <h3 v-if="hasMatchingProducts(section)">{{ section.name }}</h3>
            <ul v-if="hasMatchingProducts(section)" class="product-list">
                <li v-for="product in section.products" :key="product.id" class="product-item">
                    <div v-if="filterProduct(product) && isSearchedProduct(product)" class="product-details">
                        {{ product.name }} - {{ product.unit_type }} - Rate: {{ product.rate_per_unit }}
                        - Quantity Available: {{ product.quantity_available }}
                        <button v-if="!product.addedToCart && product.quantity_available > 0" @click="addToCart(product)">
                            Add to Cart
                        </button>
                        <button v-else-if="product.quantity_available > 0">
                            Added
                        </button>
                        <button v-else disabled>
                            Out of Stock
                        </button>
                    </div>
                </li>
            </ul>
        </div>
        <button @click="toggleCart" class="cart-button">View Cart</button>
        <Cart v-if="showCart" :cart="cart" @updateCart="updateCart" />
        <br/>
        <RouterLink to="/order-history" class="order-history-link">View Order History</RouterLink>
    </div>
</template>

<script>
import axios from 'axios';
import Cart from '../components/CartItems.vue'
import { RouterLink } from 'vue-router';
// import Vue from 'vue';
export default {
    data() {
        return {
            sections: [],
            cart: {},
            filter: {
                sectionId: "All",
                maxPrice: "Infinity",
            },
            searchProduct: "",
            showCart: false,
        };
    },
    created() {
        this.fetchSections();
    },
    methods: {
        toggleCart() {
            this.showCart = !this.showCart;
        },
        fetchSections() {
            const accessToken = localStorage.getItem('access_token');
            axios
                .get('/api/sections', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.sections = response.data;
                })
                .catch((error) => {
                    console.error('Failed to fetch sections:', error);
                });
        },
        filterProduct(product) {
            const sectionFilter = this.filter.sectionId === 'All' || product.section_id === this.filter.sectionId;
            const priceFilter = product.rate_per_unit <= this.filter.maxPrice;
            return sectionFilter && priceFilter;
        },
        isSearchedProduct(product) {
            // Check if the product matches the search criteria
            const searchText = this.searchProduct.trim();
            if (searchText) {
                // If search text is not empty, check if the product name contains the search text
                return product.name.toLowerCase().includes(searchText.toLowerCase());
            }
            // If search text is empty, all products should be displayed
            return true;
        },
        hasMatchingProducts(section) {
            // Check if the section has products that match the search criteria
            return section.products.some((product) => this.filterProduct(product) && this.isSearchedProduct(product));
        },
        addToCart(product) {
            if (product.quantity_available > 0) {
                if (!this.cart[product.id]) {
                    this.cart[product.id] = {
                        id: product.id,
                        productName: product.name,
                        price: product.rate_per_unit,
                        quantity: 1,
                        available: product.quantity_available,
                    };
                    product.addedToCart = true; // Mark the product as added to the cart
                } else {
                    this.cart[product.id].quantity += 1;
                    this.cart[product.id].available -= 1;
                }
                product.quantity_available -= 1;
                this.cart = { ...this.cart }; // Update the parent's cart

                // Update the view if the product is added to the cart
                this.updateAvailableQuantities();
            }
        },
        updateCart(cart) {
            this.cart = { ...cart };
            this.updateAvailableQuantities();
        },
        updateAvailableQuantities() {
            // Loop through the sections and products, updating the available quantities based on the cart
            this.sections.forEach((section) => {
                section.products.forEach((product) => {
                    if (this.cart[product.id]) {
                        product.quantity_available = this.cart[product.id].available;
                    }
                });
            });
        },
        logout() {
            // Remove the access token from local storage
            localStorage.removeItem('access_token');

            // Redirect to the login page or any other desired page after logout
            this.$router.push('/login');
        },
    },
    watch: {
        'filter.maxPrice': function (newMaxPrice) {
            if (!newMaxPrice) {
                this.filter.maxPrice = "Infinity";
            }
        },
        cart: {
            handler: 'updateAvailableQuantities',
        },
    },
    components: {
    Cart,
    RouterLink
},
};
</script>

<style scoped>
.dashboard-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.logout-button,
.cart-button {
    background-color: #e74c3c;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-bottom: 10px;
}

.logout-button:hover,
.cart-button:hover {
    background-color: #c0392b;
}

.filter-section {
    margin-bottom: 15px;
}

.filter-select,
.filter-input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    margin-top: 5px;
}

.product-section {
    margin-top: 20px;
}

.product-list {
    list-style: none;
    padding: 0;
}

.product-item {
    margin-bottom: 10px;
}

.product-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-details button {
    background-color: #3498db;
    color: white;
    padding: 5px 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.product-details button:hover {
    background-color: #2980b9;
}

.cart-button {
    background-color: #2ecc71;
}

.cart-button:hover {
    background-color: #27ae60;
}

.order-history-link {
    display: block;
    margin-top: 20px;
    text-decoration: none;
    color: #3498db;
}</style>
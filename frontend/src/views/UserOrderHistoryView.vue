<template>
    <div class="order-history-container">
        <h2>User Order History</h2>
        <div v-for="order in orderHistory" :key="order.order_id" class="order-details">
            <h3>Order ID: {{ order.order_id }}</h3>
            <p>Timestamp: {{ order.timestamp }}</p>
            <ul class="order-items">
                <li v-for="item in order.items" :key="item.product_name" class="order-item">
                    {{ item.product_name }} - Quantity: {{ item.quantity }} - Price: {{ item.price }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            orderHistory: [],
        };
    },
    mounted() {
        this.fetchOrderHistory();
    },
    methods: {
        async fetchOrderHistory() {
            try {
                const response = await axios.get(`/api/user/order-history`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                    },
                });
                this.orderHistory = response.data;
            } catch (error) {
                console.error('Error fetching order history:', error.message);
            }
        },
    },
};
</script>

<style scoped>
.order-history-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.order-details {
    margin-top: 20px;
}

.order-details h3 {
    color: #3498db;
}

.order-items {
    list-style: none;
    padding: 0;
    margin-top: 10px;
}

.order-item {
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px solid #ddd;
}

@media only screen and (max-width: 600px) {
    .order-details {
        margin-top: 15px;
    }

    .order-items {
        margin-top: 8px;
    }

    .order-item {
        margin-bottom: 8px;
    }
}
</style>
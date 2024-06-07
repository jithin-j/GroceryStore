<template>
    <div class="admin-dashboard-container">
        <h2>Admin Dashboard</h2>
        <button @click="logout" class="logout-button">Logout</button>

        <div v-if="managerAccounts.length > 0" class="pending-accounts">
            <h3>Pending Manager Accounts</h3>
            <ul class="accounts-list">
                <li v-for="account in managerAccounts" :key="account.id" class="account-item">
                    <span class="account-name">{{ account.username }}</span>
                    <div class="button-group">
                        <button @click="approveAccount(account.id)" class="approve-button">Approve</button>
                        <button @click="rejectAccount(account.id)" class="reject-button">Reject</button>
                    </div>
                </li>
            </ul>
        </div>

        <div v-else>
            <p>No pending manager accounts.</p>
        </div>

        <RouterLink to="/sections" class="dashboard-link">View Sections</RouterLink>
        <br />
        <RouterLink to="/section/add" class="dashboard-link">Add a new section</RouterLink>
        <br />
        <RouterLink to="/section-requests" class="dashboard-link">View Section Requests</RouterLink>
    </div>
</template>

<style scoped>
.admin-dashboard-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.logout-button {
    background-color: #e74c3c;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    margin-bottom: 20px;
}

.logout-button:hover {
    background-color: #c0392b;
}

.pending-accounts {
    margin-top: 20px;
}

.accounts-list {
    list-style: none;
    padding: 0;
}

.account-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding: 10px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 3px;
}

.account-name {
    color: black;
}

.button-group {
    display: flex;
    gap: 10px;
    /* Increased gap between buttons */
}

.approve-button,
.reject-button,
.dashboard-link {
    background-color: #3498db;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    text-decoration: none;
}

.approve-button:hover,
.reject-button:hover,
.dashboard-link:hover {
    background-color: #2980b9;
}
</style>


<script>
import axios from "axios";
import { RouterLink } from "vue-router";
export default {
    data() {
        return {
            managerAccounts: [],
        };
    },
    created() {
        // Fetch a list of pending manager accounts from your API
        // You can use Axios or a similar library for this.
        // Update the managerAccounts data with the fetched data.
        const jwtToken = localStorage.getItem('access_token');
        axios
            .get("/api/manager-accounts/pending", {
            headers: {
                Authorization: `Bearer ${jwtToken}`,
            },
        })
            .then((response) => {
            this.managerAccounts = response.data;
        })
            .catch((error) => {
            console.error("Failed to fetch pending manager accounts:", error);
        });
    },
    methods: {
        approveAccount(accountId) {
            const jwtToken = localStorage.getItem("access_token");
            axios
                .post(`/admin/approve_manager/${accountId}/approve`, null, {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            })
                .then(() => {
                this.managerAccounts = this.managerAccounts.filter((item) => item.id !== accountId);
            })
                .catch((error) => {
                console.error("Failed to approve manager account:", error);
            });
        },
        rejectAccount(accountId) {
            const jwtToken = localStorage.getItem("access_token");
            axios
                .post(`/admin/approve_manager/${accountId}/reject`, null, {
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            })
                .then(() => {
                // Remove the rejected account from the list
                this.managerAccounts = this.managerAccounts.filter((item) => item.id !== accountId);
            })
                .catch((error) => {
                console.error("Failed to reject manager account:", error);
            });
        },
        logout() {
            // Remove the access token from local storage
            localStorage.removeItem('access_token');

            // Redirect to the login page or any other desired page after logout
            this.$router.push('/admin/login');
        },
    },
    components: { RouterLink }
};
</script>

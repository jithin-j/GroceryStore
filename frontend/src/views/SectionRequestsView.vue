<template>
    <div class="section-requests-container">
        <h2>Section Requests</h2>
        <ul class="requests-list">
            <li v-for="request in sectionRequests" :key="request.id" class="request-item">
                <span class="section-name">{{ request.section_name }}</span>
                <br />
                <span>Request Type: {{ request.request_type }}</span>
                <div class="button-group">
                    <button @click="acceptRequest(request.id)" class="accept-button">Accept</button>
                    <button @click="rejectRequest(request.id)" class="reject-button">Reject</button>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.section-requests-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

h2 {
    margin-bottom: 20px;
}

.requests-list {
    list-style: none;
    padding: 0;
}

.request-item {
    padding: 15px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 10px;
    color: black;
}

.section-name {
    font-weight: bold;
    color: black;
}

.button-group {
    display: flex;
    gap: 10px;
}

.accept-button,
.reject-button {
    background-color: #3498db;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.accept-button:hover,
.reject-button:hover {
    background-color: #2980b9;
}
</style>


<script>
import axios from "axios";

export default {
    data() {
        return {
            sectionRequests: [],
        };
    },
    created() {
        this.fetchSectionRequests();
    },
    methods: {
        fetchSectionRequests() {
            const jwtToken = localStorage.getItem("access_token");

            if (jwtToken) {
                const config = {
                    headers: {
                        Authorization: `Bearer ${jwtToken}`,
                    },
                };

                axios.get("/api/section-requests", config).then((response) => {
                    this.sectionRequests = response.data;
                });
            }
        },
        acceptRequest(requestId) {
            const jwtToken = localStorage.getItem("access_token");

            if (jwtToken) {
                const config = {
                    headers: {
                        Authorization: `Bearer ${jwtToken}`,
                    },
                };

                axios.put(`/api/section-requests/approve/${requestId}`, null, config).then(() => {
                    this.sectionRequests = this.sectionRequests.filter((request) => request.id !== requestId);
                });
            }
        },
        rejectRequest(requestId) {
            const jwtToken = localStorage.getItem("access_token");

            if (jwtToken) {
                const config = {
                    headers: {
                        Authorization: `Bearer ${jwtToken}`,
                    },
                };

                axios.put(`/api/section-requests/reject/${requestId}`, null, config).then(() => {
                    this.sectionRequests = this.sectionRequests.filter((request) => request.id !== requestId);
                });
            }
        },
    },
};
</script>
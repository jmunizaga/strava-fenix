import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const rankingsApi = {
    async getWeeklyRankings(gender = null, weekOffset = -1) {
        const params = { week_offset: weekOffset };
        if (gender) {
            params.gender = gender;
        }

        const response = await api.get('/api/rankings/weekly', { params });
        return response.data;
    },



    /**
     * Get Strava login URL
     */
    async getLoginUrl() {
        const response = await api.get('/api/auth/login');
        return response.data.url;
    },

    /**
     * Send auth code to backend
     */
    async sendAuthCallback(code) {
        const response = await api.post('/api/auth/callback', { code });
        return response.data;
    },
};

export default api;

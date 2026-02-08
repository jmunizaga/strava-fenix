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
    /**
     * Get weekly rankings
     * @param {string} category - Category code (general, elite, amateur, master_a, etc.)
     * @param {string|null} gender - Gender filter (M, F, or null for all)
     * @param {number} weekOffset - Week offset (0=current, -1=last week)
     */
    async getWeeklyRankings(category = 'general', gender = null, weekOffset = 0) {
        const params = { category, week_offset: weekOffset };
        if (gender) {
            params.gender = gender;
        }

        const response = await api.get('/api/rankings/weekly', { params });
        return response.data;
    },

    /**
     * Get all available UCI categories
     */
    async getCategories() {
        const response = await api.get('/api/rankings/categories');
        return response.data;
    },
};

export default api;

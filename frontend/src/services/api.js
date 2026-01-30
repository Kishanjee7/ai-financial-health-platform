import axios from 'axios';

const api = axios.create({
    baseURL: '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadFinancialFile = async (file, language = 'en') => {
    const formData = new FormData();
    formData.append('file', file);

    // axios handles Content-Type automatically for FormData
    const response = await api.post(`/analysis/upload?language=${language}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });
    return response.data;
};

export default api;

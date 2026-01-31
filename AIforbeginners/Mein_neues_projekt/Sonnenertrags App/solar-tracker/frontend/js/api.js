// API Helper Functions

const API_BASE = '/api';

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const response = await fetch(url, { ...defaultOptions, ...options });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
}

// Readings API
const readingsApi = {
    getAll: () => apiRequest('/readings'),
    getStatistics: () => apiRequest('/readings/statistics'),
    getMonthlyComparison: () => apiRequest('/readings/monthly-comparison'),
    create: (data) => apiRequest('/readings', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    delete: (id) => apiRequest(`/readings/${id}`, { method: 'DELETE' }),
    importExcel: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch(`${API_BASE}/readings/import-excel`, {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
            throw new Error(error.detail);
        }
        return response.json();
    }
};

// Settings API
const settingsApi = {
    getAll: () => apiRequest('/settings'),
    update: (key, value) => apiRequest('/settings', {
        method: 'PUT',
        body: JSON.stringify({ key, value })
    }),
    updateBulk: (settings) => apiRequest('/settings/bulk', {
        method: 'PUT',
        body: JSON.stringify(settings)
    })
};

// Reference API
const referenceApi = {
    getPvgis: (lat, lon, peakpower) =>
        apiRequest(`/reference/pvgis?lat=${lat}&lon=${lon}&peakpower=${peakpower}`),
    getTypicalYields: () => apiRequest('/reference/typical-yields')
};

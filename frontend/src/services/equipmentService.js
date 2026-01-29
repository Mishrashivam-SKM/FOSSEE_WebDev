import api from './api';

/**
 * Equipment/Dataset service for handling data operations
 */
const equipmentService = {
  /**
   * Get all datasets for the current user
   */
  async getDatasets() {
    const response = await api.get('/datasets/');
    return response.data;
  },

  /**
   * Get a specific dataset by ID
   */
  async getDataset(id) {
    const response = await api.get(`/datasets/${id}/`);
    return response.data;
  },

  /**
   * Upload a new CSV file
   */
  async uploadFile(file, name = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (name) {
      formData.append('name', name);
    }

    const response = await api.post('/datasets/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Delete a dataset
   */
  async deleteDataset(id) {
    await api.delete(`/datasets/${id}/`);
    return { success: true };
  },

  /**
   * Get analytics for a dataset
   */
  async getAnalytics(datasetId) {
    const response = await api.get(`/datasets/${datasetId}/analytics/`);
    return response.data;
  },

  /**
   * Get equipment items for a dataset
   */
  async getEquipment(datasetId) {
    const response = await api.get(`/datasets/${datasetId}/equipment/`);
    return response.data;
  },

  /**
   * Download PDF report for a dataset
   */
  async downloadPDF(datasetId) {
    const response = await api.get(`/datasets/${datasetId}/pdf/`, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    return { success: true };
  },

  /**
   * Get combined dashboard analytics for ALL datasets
   */
  async getDashboardAnalytics() {
    const response = await api.get('/datasets/dashboard/');
    return response.data;
  },

  /**
   * Get all equipment items (optionally filtered)
   */
  async getAllEquipment(params = {}) {
    const response = await api.get('/equipment/', { params });
    return response.data;
  },
};

export default equipmentService;

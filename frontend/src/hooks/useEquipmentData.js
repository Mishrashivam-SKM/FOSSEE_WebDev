import { useState, useCallback } from 'react';
import equipmentService from '../services/equipmentService';

export const useEquipmentData = () => {
  const [datasets, setDatasets] = useState([]);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [dashboardAnalytics, setDashboardAnalytics] = useState(null);
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDatasets = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.getDatasets();
      setDatasets(data.results || []);
      return data;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch datasets');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchDataset = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.getDataset(id);
      setCurrentDataset(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch dataset');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAnalytics = useCallback(async (datasetId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.getAnalytics(datasetId);
      setAnalytics(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch analytics');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchEquipment = useCallback(async (datasetId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.getEquipment(datasetId);
      setEquipment(data.equipment || []);
      return data;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch equipment');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const uploadFile = useCallback(async (file, name) => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.uploadFile(file, name);
      // Refresh datasets after upload
      await fetchDatasets();
      return data;
    } catch (err) {
      setError(err.response?.data?.errors?.join(', ') || 'Failed to upload file');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchDatasets]);

  const deleteDataset = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    try {
      await equipmentService.deleteDataset(id);
      // Refresh datasets after delete
      await fetchDatasets();
      return { success: true };
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete dataset');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchDatasets]);

  const downloadPDF = useCallback(async (datasetId) => {
    setLoading(true);
    setError(null);
    try {
      await equipmentService.downloadPDF(datasetId);
      return { success: true };
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to download PDF');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchDashboardAnalytics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await equipmentService.getDashboardAnalytics();
      setDashboardAnalytics(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch dashboard analytics');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    datasets,
    currentDataset,
    analytics,
    dashboardAnalytics,
    equipment,
    loading,
    error,
    fetchDatasets,
    fetchDataset,
    fetchAnalytics,
    fetchDashboardAnalytics,
    fetchEquipment,
    uploadFile,
    deleteDataset,
    downloadPDF,
    setError,
  };
};

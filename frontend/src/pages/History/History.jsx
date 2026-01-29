import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useEquipmentData } from '../../hooks/useEquipmentData';
import { formatDate } from '../../utils/formatters';
import toast from 'react-hot-toast';
import { FiEye, FiDownload, FiTrash2, FiDatabase, FiUpload } from 'react-icons/fi';
import './History.css';

const History = () => {
  const navigate = useNavigate();
  const { datasets, fetchDatasets, deleteDataset, downloadPDF, loading } = useEquipmentData();
  const [deletingId, setDeletingId] = useState(null);
  const [downloadingId, setDownloadingId] = useState(null);

  useEffect(() => {
    fetchDatasets();
  }, [fetchDatasets]);

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) {
      return;
    }

    setDeletingId(id);
    try {
      await deleteDataset(id);
      toast.success('Dataset deleted successfully');
    } catch (error) {
      toast.error('Failed to delete dataset');
    } finally {
      setDeletingId(null);
    }
  };

  const handleDownload = async (id) => {
    setDownloadingId(id);
    try {
      await downloadPDF(id);
      toast.success('PDF report downloaded');
    } catch (error) {
      toast.error('Failed to download PDF');
    } finally {
      setDownloadingId(null);
    }
  };

  const handleView = (id) => {
    navigate(`/analysis/${id}`);
  };

  if (loading && datasets.length === 0) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Upload History</h1>
          <p className="page-subtitle">View and manage your uploaded datasets (max 5 stored)</p>
        </div>
        <Link to="/upload" className="btn btn-primary">
          <FiUpload />
          <span>Upload New</span>
        </Link>
      </div>

      {datasets.length === 0 ? (
        <div className="empty-state">
          <FiDatabase className="empty-icon" />
          <h3>No Datasets Yet</h3>
          <p>You haven't uploaded any data files. Get started by uploading your first CSV.</p>
          <Link to="/upload" className="btn btn-primary">
            Upload Data
          </Link>
        </div>
      ) : (
        <div className="datasets-list">
          {datasets.map((dataset) => (
            <div key={dataset.id} className="dataset-card">
              <div className="dataset-info">
                <div className="dataset-icon">
                  <FiDatabase />
                </div>
                <div className="dataset-details">
                  <h3 className="dataset-name">{dataset.name}</h3>
                  <div className="dataset-meta">
                    <span className="meta-item">
                      <strong>{dataset.row_count}</strong> equipment records
                    </span>
                    <span className="meta-separator">•</span>
                    <span className="meta-item">
                      Uploaded {formatDate(dataset.uploaded_at)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="dataset-actions">
                <button
                  className="action-btn view-btn"
                  onClick={() => handleView(dataset.id)}
                  title="View Analysis"
                >
                  <FiEye />
                  <span>View</span>
                </button>

                <button
                  className="action-btn download-btn"
                  onClick={() => handleDownload(dataset.id)}
                  disabled={downloadingId === dataset.id}
                  title="Download PDF Report"
                >
                  {downloadingId === dataset.id ? (
                    <span className="loader-tiny"></span>
                  ) : (
                    <FiDownload />
                  )}
                  <span>PDF</span>
                </button>

                <button
                  className="action-btn delete-btn"
                  onClick={() => handleDelete(dataset.id, dataset.name)}
                  disabled={deletingId === dataset.id}
                  title="Delete Dataset"
                >
                  {deletingId === dataset.id ? (
                    <span className="loader-tiny"></span>
                  ) : (
                    <FiTrash2 />
                  )}
                  <span>Delete</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="history-note">
        <p>
          <strong>Note:</strong> Only the last 5 uploaded datasets are stored. 
          Older datasets are automatically removed when new ones are uploaded.
        </p>
      </div>
    </div>
  );
};

export default History;

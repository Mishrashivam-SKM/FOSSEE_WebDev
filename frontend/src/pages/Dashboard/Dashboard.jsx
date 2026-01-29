import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useEquipmentData } from '../../hooks/useEquipmentData';
import BarChart from '../../components/charts/BarChart';
import PieChart from '../../components/charts/PieChart';
import { formatDate, formatNumber } from '../../utils/formatters';
import { FiUpload, FiDatabase, FiTrendingUp, FiActivity, FiLayers } from 'react-icons/fi';
import './Dashboard.css';

const Dashboard = () => {
  const { 
    datasets, 
    analytics, 
    dashboardAnalytics,
    fetchDatasets, 
    fetchAnalytics, 
    fetchDashboardAnalytics,
    loading 
  } = useEquipmentData();
  
  const [viewMode, setViewMode] = useState('combined');
  const [selectedDatasetId, setSelectedDatasetId] = useState(null);

  useEffect(() => {
    fetchDatasets();
    fetchDashboardAnalytics();
  }, [fetchDatasets, fetchDashboardAnalytics]);

  useEffect(() => {
    if (datasets.length > 0 && !selectedDatasetId) {
      setSelectedDatasetId(datasets[0].id);
    }
  }, [datasets, selectedDatasetId]);

  useEffect(() => {
    if (viewMode === 'specific' && selectedDatasetId) {
      fetchAnalytics(selectedDatasetId);
    }
  }, [viewMode, selectedDatasetId, fetchAnalytics]);

  const currentAnalytics = viewMode === 'combined' ? dashboardAnalytics : analytics;
  const selectedDataset = datasets.find(d => d.id === selectedDatasetId);

  if (loading && datasets.length === 0) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Overview of your chemical equipment data</p>
        </div>
      </div>

      {datasets.length > 0 && (
        <div className="view-toggle-container">
          <div className="view-toggle">
            <button 
              className={`toggle-btn ${viewMode === 'combined' ? 'active' : ''}`}
              onClick={() => setViewMode('combined')}
            >
              <FiLayers /> All Datasets Combined
            </button>
            <button 
              className={`toggle-btn ${viewMode === 'specific' ? 'active' : ''}`}
              onClick={() => setViewMode('specific')}
            >
              <FiDatabase /> Specific Dataset
            </button>
          </div>
          
          {viewMode === 'specific' && (
            <select 
              className="dataset-select"
              value={selectedDatasetId || ''}
              onChange={(e) => setSelectedDatasetId(Number(e.target.value))}
            >
              {datasets.map(dataset => (
                <option key={dataset.id} value={dataset.id}>
                  {dataset.name} ({dataset.row_count} records)
                </option>
              ))}
            </select>
          )}
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'rgba(59, 130, 246, 0.1)' }}>
            <FiDatabase style={{ color: 'var(--color-primary)' }} />
          </div>
          <div className="stat-content">
            <span className="stat-label">
              {viewMode === 'combined' ? 'Total Datasets' : 'Dataset'}
            </span>
            <span className="stat-value">
              {viewMode === 'combined' 
                ? (dashboardAnalytics?.datasets_count || datasets.length)
                : selectedDataset?.name?.slice(0, 15) || '-'
              }
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.1)' }}>
            <FiActivity style={{ color: 'var(--color-secondary)' }} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Total Equipment</span>
            <span className="stat-value">
              {viewMode === 'combined'
                ? (dashboardAnalytics?.total_equipment || 0)
                : (currentAnalytics?.summary?.total_count || 0)
              }
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'rgba(245, 158, 11, 0.1)' }}>
            <FiTrendingUp style={{ color: 'var(--color-warning)' }} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Avg Flowrate</span>
            <span className="stat-value">
              {formatNumber(currentAnalytics?.summary?.averages?.flowrate)}
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'rgba(139, 92, 246, 0.1)' }}>
            <FiUpload style={{ color: '#8b5cf6' }} />
          </div>
          <div className="stat-content">
            <span className="stat-label">
              {viewMode === 'combined' ? 'Latest Upload' : 'Uploaded At'}
            </span>
            <span className="stat-value-small">
              {viewMode === 'combined' 
                ? (datasets[0] ? formatDate(datasets[0].uploaded_at) : 'None')
                : (selectedDataset ? formatDate(selectedDataset.uploaded_at) : 'None')
              }
            </span>
          </div>
        </div>
      </div>

      {datasets.length === 0 ? (
        <div className="empty-state">
          <FiUpload className="empty-icon" />
          <h3>No Data Yet</h3>
          <p>Upload your first CSV file to get started with equipment analysis.</p>
          <Link to="/upload" className="btn btn-primary">
            Upload Data
          </Link>
        </div>
      ) : (
        <>
          {currentAnalytics?.summary && (
            <div className="analytics-section">
              <h2 className="section-title">
                {viewMode === 'combined' 
                  ? 'Combined Analytics (All Datasets)' 
                  : `Analytics: ${selectedDataset?.name}`
                }
              </h2>
              <p className="section-subtitle">
                {viewMode === 'combined' 
                  ? `Aggregated data from ${dashboardAnalytics?.datasets_count || datasets.length} datasets`
                  : `${selectedDataset?.row_count || 0} equipment records`
                }
              </p>

              <div className="summary-grid">
                <div className="summary-card">
                  <h4>Flowrate</h4>
                  <div className="summary-stats">
                    <div className="summary-stat">
                      <span className="label">Average</span>
                      <span className="value">{formatNumber(currentAnalytics.summary.averages?.flowrate)}</span>
                    </div>
                    <div className="summary-stat">
                      <span className="label">Range</span>
                      <span className="value">
                        {formatNumber(currentAnalytics.summary.ranges?.flowrate?.min)} - {formatNumber(currentAnalytics.summary.ranges?.flowrate?.max)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="summary-card">
                  <h4>Pressure</h4>
                  <div className="summary-stats">
                    <div className="summary-stat">
                      <span className="label">Average</span>
                      <span className="value">{formatNumber(currentAnalytics.summary.averages?.pressure)}</span>
                    </div>
                    <div className="summary-stat">
                      <span className="label">Range</span>
                      <span className="value">
                        {formatNumber(currentAnalytics.summary.ranges?.pressure?.min)} - {formatNumber(currentAnalytics.summary.ranges?.pressure?.max)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="summary-card">
                  <h4>Temperature</h4>
                  <div className="summary-stats">
                    <div className="summary-stat">
                      <span className="label">Average</span>
                      <span className="value">{formatNumber(currentAnalytics.summary.averages?.temperature)}</span>
                    </div>
                    <div className="summary-stat">
                      <span className="label">Range</span>
                      <span className="value">
                        {formatNumber(currentAnalytics.summary.ranges?.temperature?.min)} - {formatNumber(currentAnalytics.summary.ranges?.temperature?.max)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {currentAnalytics?.chart_data && (
            <div className="charts-section">
              <div className="charts-grid">
                <div className="chart-card">
                  <h3 className="chart-title">Equipment Type Distribution</h3>
                  <PieChart data={currentAnalytics.chart_data.pie_chart} title="" />
                </div>

                <div className="chart-card">
                  <h3 className="chart-title">Average Parameters by Type</h3>
                  <BarChart data={currentAnalytics.chart_data.bar_chart} title="" xLabel="Equipment Type" yLabel="Value" />
                </div>
              </div>
            </div>
          )}

          <div className="quick-actions">
            <Link to="/upload" className="action-card">
              <FiUpload className="action-icon" />
              <span>Upload New Data</span>
            </Link>
            <Link to="/history" className="action-card">
              <FiDatabase className="action-icon" />
              <span>View All Datasets</span>
            </Link>
            {selectedDatasetId && viewMode === 'specific' && (
              <Link to={`/analysis/${selectedDatasetId}`} className="action-card">
                <FiTrendingUp className="action-icon" />
                <span>Detailed Analysis</span>
              </Link>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;

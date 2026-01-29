import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useEquipmentData } from '../../hooks/useEquipmentData';
import DataTable from '../../components/common/DataTable';
import BarChart from '../../components/charts/BarChart';
import PieChart from '../../components/charts/PieChart';
import { formatDate, formatNumber } from '../../utils/formatters';
import toast from 'react-hot-toast';
import { FiDownload, FiArrowLeft, FiActivity, FiThermometer, FiDroplet } from 'react-icons/fi';
import './Analysis.css';

const Analysis = () => {
  const { datasetId } = useParams();
  const {
    currentDataset,
    analytics,
    equipment,
    fetchDataset,
    fetchAnalytics,
    fetchEquipment,
    downloadPDF,
    loading,
  } = useEquipmentData();

  const [downloading, setDownloading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (datasetId) {
      fetchDataset(datasetId);
      fetchAnalytics(datasetId);
      fetchEquipment(datasetId);
    }
  }, [datasetId, fetchDataset, fetchAnalytics, fetchEquipment]);

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      await downloadPDF(datasetId);
      toast.success('PDF report downloaded');
    } catch (error) {
      toast.error('Failed to download PDF');
    } finally {
      setDownloading(false);
    }
  };

  const equipmentColumns = [
    { key: 'name', label: 'Equipment Name', width: '25%' },
    { key: 'type', label: 'Type', width: '15%' },
    {
      key: 'flowrate',
      label: 'Flowrate',
      width: '20%',
      render: (value) => formatNumber(value),
    },
    {
      key: 'pressure',
      label: 'Pressure',
      width: '20%',
      render: (value) => formatNumber(value),
    },
    {
      key: 'temperature',
      label: 'Temperature',
      width: '20%',
      render: (value) => formatNumber(value),
    },
  ];

  if (loading && !currentDataset) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
      </div>
    );
  }

  if (!currentDataset && !loading) {
    return (
      <div className="analysis-page">
        <div className="error-state">
          <h2>Dataset Not Found</h2>
          <p>The requested dataset could not be found.</p>
          <Link to="/history" className="btn btn-primary">
            View All Datasets
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="analysis-page">
      {/* Header */}
      <div className="analysis-header">
        <div className="header-left">
          <Link to="/history" className="back-link">
            <FiArrowLeft />
            <span>Back to History</span>
          </Link>
          <h1 className="page-title">{currentDataset?.name}</h1>
          <p className="page-subtitle">
            {currentDataset?.row_count} equipment records • 
            Uploaded {formatDate(currentDataset?.uploaded_at)}
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={handleDownloadPDF}
          disabled={downloading}
        >
          {downloading ? (
            <span className="loader-small"></span>
          ) : (
            <FiDownload />
          )}
          <span>Download PDF Report</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'charts' ? 'active' : ''}`}
          onClick={() => setActiveTab('charts')}
        >
          Charts
        </button>
        <button
          className={`tab ${activeTab === 'data' ? 'active' : ''}`}
          onClick={() => setActiveTab('data')}
        >
          Data Table
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && analytics?.summary && (
          <div className="overview-tab">
            {/* Summary Stats */}
            <div className="stats-row">
              <div className="stat-card">
                <div className="stat-icon-large" style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--color-primary)' }}>
                  <FiActivity />
                </div>
                <div className="stat-content">
                  <span className="stat-value">{analytics.summary.total_count}</span>
                  <span className="stat-label">Total Equipment</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon-large" style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--color-primary)' }}>
                  <FiDroplet />
                </div>
                <div className="stat-content">
                  <span className="stat-value">{formatNumber(analytics.summary.averages.flowrate)}</span>
                  <span className="stat-label">Avg Flowrate</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon-large" style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--color-secondary)' }}>
                  <FiActivity />
                </div>
                <div className="stat-content">
                  <span className="stat-value">{formatNumber(analytics.summary.averages.pressure)}</span>
                  <span className="stat-label">Avg Pressure</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon-large" style={{ background: 'rgba(245, 158, 11, 0.1)', color: 'var(--color-warning)' }}>
                  <FiThermometer />
                </div>
                <div className="stat-content">
                  <span className="stat-value">{formatNumber(analytics.summary.averages.temperature)}</span>
                  <span className="stat-label">Avg Temperature</span>
                </div>
              </div>
            </div>

            {/* Type Distribution */}
            <div className="distribution-section">
              <h3>Equipment Type Distribution</h3>
              <div className="distribution-grid">
                {Object.entries(analytics.summary.type_distribution).map(([type, count]) => (
                  <div key={type} className="distribution-item">
                    <span className="distribution-type">{type}</span>
                    <span className="distribution-count">{count}</span>
                    <span className="distribution-percent">
                      {((count / analytics.summary.total_count) * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Ranges Table */}
            <div className="ranges-section">
              <h3>Parameter Ranges</h3>
              <div className="ranges-table">
                <div className="range-row header">
                  <span>Parameter</span>
                  <span>Min</span>
                  <span>Max</span>
                  <span>Average</span>
                </div>
                <div className="range-row">
                  <span>Flowrate</span>
                  <span>{formatNumber(analytics.summary.ranges.flowrate.min)}</span>
                  <span>{formatNumber(analytics.summary.ranges.flowrate.max)}</span>
                  <span>{formatNumber(analytics.summary.averages.flowrate)}</span>
                </div>
                <div className="range-row">
                  <span>Pressure</span>
                  <span>{formatNumber(analytics.summary.ranges.pressure.min)}</span>
                  <span>{formatNumber(analytics.summary.ranges.pressure.max)}</span>
                  <span>{formatNumber(analytics.summary.averages.pressure)}</span>
                </div>
                <div className="range-row">
                  <span>Temperature</span>
                  <span>{formatNumber(analytics.summary.ranges.temperature.min)}</span>
                  <span>{formatNumber(analytics.summary.ranges.temperature.max)}</span>
                  <span>{formatNumber(analytics.summary.averages.temperature)}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'charts' && analytics?.chart_data && (
          <div className="charts-tab">
            <div className="charts-grid">
              <div className="chart-card">
                <h3>Equipment Type Distribution</h3>
                <PieChart data={analytics.chart_data.pie_chart} />
              </div>
              <div className="chart-card">
                <h3>Average Parameters by Type</h3>
                <BarChart
                  data={analytics.chart_data.bar_chart}
                  xLabel="Equipment Type"
                  yLabel="Value"
                />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'data' && (
          <div className="data-tab">
            <DataTable
              columns={equipmentColumns}
              data={equipment}
              loading={loading}
              emptyMessage="No equipment data available"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Analysis;

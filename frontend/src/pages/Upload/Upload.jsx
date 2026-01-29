import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useEquipmentData } from '../../hooks/useEquipmentData';
import { useFileUpload } from '../../hooks/useFileUpload';
import FileUpload from '../../components/common/FileUpload';
import toast from 'react-hot-toast';
import { FiUploadCloud, FiCheck } from 'react-icons/fi';
import './Upload.css';

const Upload = () => {
  const navigate = useNavigate();
  const { uploadFile, loading } = useEquipmentData();
  const {
    file,
    error: fileError,
    isDragging,
    handleDragEnter,
    handleDragLeave,
    handleDragOver,
    handleDrop,
    clearFile,
  } = useFileUpload();

  const [customName, setCustomName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [localError, setLocalError] = useState(null);

  const handleFileSelect = (newFile) => {
    setSelectedFile(newFile);
    setLocalError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      toast.error('Please select a CSV file to upload');
      return;
    }

    try {
      const response = await uploadFile(selectedFile, customName || selectedFile.name);
      
      if (response.success) {
        toast.success(`Successfully uploaded ${response.dataset.row_count} equipment records!`);
        
        if (response.warnings && response.warnings.length > 0) {
          response.warnings.forEach((warning) => {
            toast(warning, { icon: null });
          });
        }
        
        // Navigate to analysis page for the new dataset
        navigate(`/analysis/${response.dataset_id}`);
      }
    } catch (error) {
      const errors = error.response?.data?.errors;
      if (errors) {
        errors.forEach((err) => toast.error(err));
      } else {
        toast.error('Failed to upload file');
      }
    }
  };

  return (
    <div className="upload-page">
      <div className="page-header">
        <h1 className="page-title">Upload Data</h1>
        <p className="page-subtitle">
          Upload a CSV file containing chemical equipment data
        </p>
      </div>

      <div className="upload-container">
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="upload-section">
            <h3 className="section-label">Select CSV File</h3>
            <FileUpload
              file={selectedFile}
              error={localError || fileError}
              isDragging={isDragging}
              onFileSelect={handleFileSelect}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={(e) => {
                handleDrop(e);
                const droppedFile = e.dataTransfer.files?.[0];
                if (droppedFile) handleFileSelect(droppedFile);
              }}
              onClear={() => {
                clearFile();
                setSelectedFile(null);
              }}
              disabled={loading}
            />
          </div>

          <div className="upload-section">
            <label className="form-label">Dataset Name (Optional)</label>
            <input
              type="text"
              className="form-input"
              placeholder="Enter a custom name for this dataset"
              value={customName}
              onChange={(e) => setCustomName(e.target.value)}
              disabled={loading}
            />
            <p className="form-hint">
              Leave blank to use the original filename
            </p>
          </div>

          <div className="upload-info">
            <h4>Expected CSV Format</h4>
            <p>Your CSV file should contain the following columns:</p>
            <ul>
              <li><strong>Equipment Name</strong> - Unique identifier for each equipment</li>
              <li><strong>Type</strong> - Equipment type (e.g., Pump, Compressor, Valve)</li>
              <li><strong>Flowrate</strong> - Flow rate measurement (numeric)</li>
              <li><strong>Pressure</strong> - Pressure measurement (numeric)</li>
              <li><strong>Temperature</strong> - Temperature measurement (numeric)</li>
            </ul>
          </div>

          <button
            type="submit"
            className="btn btn-primary upload-btn"
            disabled={loading || !selectedFile}
          >
            {loading ? (
              <>
                <span className="loader-small"></span>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <FiUploadCloud />
                <span>Upload & Analyze</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Upload;

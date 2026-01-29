import { useRef } from 'react';
import { FiUploadCloud, FiFile, FiX } from 'react-icons/fi';
import { formatFileSize } from '../../../utils/formatters';
import './FileUpload.css';

const FileUpload = ({
  file,
  error,
  isDragging,
  onFileSelect,
  onDragEnter,
  onDragLeave,
  onDragOver,
  onDrop,
  onClear,
  disabled = false,
}) => {
  const inputRef = useRef(null);

  const handleClick = () => {
    if (!disabled) {
      inputRef.current?.click();
    }
  };

  const handleInputChange = (event) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  };

  return (
    <div className="file-upload-container">
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        onChange={handleInputChange}
        className="file-input-hidden"
        disabled={disabled}
      />

      {file ? (
        <div className="file-preview">
          <div className="file-info">
            <FiFile className="file-icon" />
            <div className="file-details">
              <span className="file-name">{file.name}</span>
              <span className="file-size">{formatFileSize(file.size)}</span>
            </div>
          </div>
          <button
            type="button"
            className="clear-btn"
            onClick={onClear}
            disabled={disabled}
          >
            <FiX />
          </button>
        </div>
      ) : (
        <div
          className={`dropzone ${isDragging ? 'dragging' : ''} ${disabled ? 'disabled' : ''}`}
          onClick={handleClick}
          onDragEnter={onDragEnter}
          onDragLeave={onDragLeave}
          onDragOver={onDragOver}
          onDrop={onDrop}
        >
          <FiUploadCloud className="upload-icon" />
          <p className="dropzone-text">
            <span className="highlight">Click to upload</span> or drag and drop
          </p>
          <p className="dropzone-hint">CSV files only (max 10MB)</p>
        </div>
      )}

      {error && <p className="file-error">{error}</p>}
    </div>
  );
};

export default FileUpload;

import { useState, useCallback, useRef } from 'react';

export const useFileUpload = (options = {}) => {
  const { maxSize = 10 * 1024 * 1024, allowedTypes = ['.csv'] } = options;
  
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const validateFile = useCallback((file) => {
    // Check file type
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(extension)) {
      return `Invalid file type. Allowed: ${allowedTypes.join(', ')}`;
    }

    // Check file size
    if (file.size > maxSize) {
      return `File too large. Maximum size: ${(maxSize / 1024 / 1024).toFixed(1)}MB`;
    }

    return null;
  }, [allowedTypes, maxSize]);

  const handleFileSelect = useCallback((selectedFile) => {
    setError(null);
    
    if (!selectedFile) {
      setFile(null);
      return;
    }

    const validationError = validateFile(selectedFile);
    if (validationError) {
      setError(validationError);
      setFile(null);
      return;
    }

    setFile(selectedFile);
  }, [validateFile]);

  const handleInputChange = useCallback((event) => {
    const selectedFile = event.target.files?.[0];
    handleFileSelect(selectedFile);
  }, [handleFileSelect]);

  const handleDragEnter = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
  }, []);

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];
    handleFileSelect(droppedFile);
  }, [handleFileSelect]);

  const openFileDialog = useCallback(() => {
    inputRef.current?.click();
  }, []);

  const clearFile = useCallback(() => {
    setFile(null);
    setError(null);
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  }, []);

  return {
    file,
    error,
    isDragging,
    inputRef,
    handleInputChange,
    handleDragEnter,
    handleDragLeave,
    handleDragOver,
    handleDrop,
    openFileDialog,
    clearFile,
  };
};

import React, { useState } from 'react';
import { uploadFinancialFile } from '../services/api';

const FileUpload = ({ onUploadSuccess, language = 'en' }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError(null);
    };

    const handleUpload = async () => {
        if (!file) return;

        setLoading(true);
        setError(null);
        try {
            const data = await uploadFinancialFile(file, language);
            onUploadSuccess(data);
        } catch (err) {
            console.error(err);
            setError("Failed to upload file. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card glass-card upload-component">
            <h3>Upload Financial Records</h3>
            <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
                Upload your CSV, Excel, or PDF statements.
            </p>

            <input
                type="file"
                onChange={handleFileChange}
                accept=".csv,.xlsx,.xls,.pdf"
                style={{ marginBottom: '1rem', color: 'var(--text-main)' }}
            />

            {error && <div style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</div>}

            <button
                className="primary-btn"
                onClick={handleUpload}
                disabled={!file || loading}
            >
                {loading ? 'Analyzing...' : 'Analyze Financials'}
            </button>
        </div>
    );
};

export default FileUpload;

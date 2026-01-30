import { useState } from 'react'
import './App.css'
import FileUpload from './components/FileUpload'
import ReportView from './components/ReportView'

function App() {
    const [report, setReport] = useState(null);
    const [language, setLanguage] = useState('en'); // 'en' or 'hi'

    return (
        <div className="app-container">
            <nav className="navbar">
                <div className="logo">FinHealth AI</div>
                <div className="nav-links">
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="lang-select"
                        style={{ padding: '0.5rem', borderRadius: '8px', border: '1px solid var(--glass-border)', background: 'rgba(255,255,255,0.1)', color: 'white' }}
                    >
                        <option value="en">English</option>
                        <option value="hi">Hindi (हिंदी)</option>
                    </select>
                    <a href="#" onClick={() => setReport(null)} className={!report ? "active" : ""}>Dashboard</a>
                    {report && <a href="#" className="active">Report</a>}
                </div>
            </nav>

            <main className="main-content">
                {!report ? (
                    <FileUpload setReport={setReport} language={language} />
                ) : (
                    <ReportView report={report} language={language} />
                )}
            </main>
        </div >
    )
}

export default App

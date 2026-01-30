import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const ReportView = ({ report }) => {
    if (!report) return null;

    const {
        revenue_streams, cost_structure, key_metrics,
        accounts_receivable, accounts_payable, inventory_levels,
        loan_obligations, tax_compliance,
        risk_assessment, recommendations
    } = report;

    // Transform data for charts
    const chartData = [
        { name: 'Revenue', amount: revenue_streams?.total || 0 },
        { name: 'Expected', amount: (revenue_streams?.total || 0) + (accounts_receivable?.total || 0) }
    ];

    const pieData = Object.entries(revenue_streams?.categories || {}).map(([key, value]) => ({
        name: key,
        value: value
    }));

    return (
        <div className="report-view fade-in">
            {/* High Level Summary */}
            <div className="grid-layout" style={{ marginBottom: '2rem' }}>
                <div className="card glass-card">
                    <h3>Risk Level</h3>
                    <div className={`risk-indicator ${risk_assessment === 'Low' ? 'low-risk' : 'high-risk'}`}>
                        {risk_assessment}
                    </div>
                </div>
                <div className="card glass-card">
                    <h3>Net Profit</h3>
                    <div className="risk-indicator" style={{ color: 'var(--text-main)' }}>
                        ${key_metrics?.net_profit?.toLocaleString()}
                    </div>
                </div>
                <div className="card glass-card">
                    <h3>Credit Score Est.</h3>
                    <div className="risk-indicator" style={{ color: 'var(--primary)' }}>
                        {report.credit_score_estimate}
                    </div>
                </div>
            </div>

            {/* AI Recommendations */}
            <div className="card glass-card wide" style={{ marginBottom: '2rem' }}>
                <h3>AI Recommendations</h3>
                <ul className="recommendations-list">
                    {recommendations?.map((rec, index) => (
                        <li key={index} style={{ marginBottom: '0.8rem', display: 'flex', alignItems: 'center' }}>
                            <span style={{ color: 'var(--accent)', marginRight: '0.8rem', fontSize: '1.2rem' }}>•</span>
                            <span>{rec}</span>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Detailed Dimensions Grid */}
            <h3 style={{ marginBottom: '1rem' }}>Financial Components</h3>
            <div className="grid-layout">

                {/* Revenue Breakdown */}
                <div className="card glass-card">
                    <h3>Revenue Breakdown</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Total: ${revenue_streams?.total.toLocaleString()}</p>
                    <div style={{ width: '100%', height: 200 }}>
                        <ResponsiveContainer>
                            <PieChart>
                                <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60}>
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Cash Flow Obligations */}
                <div className="card glass-card">
                    <h3>Obligations & Assets</h3>
                    <div className="stat-row">
                        <span>Receivables (AR):</span>
                        <span style={{ color: 'var(--success)' }}>+${accounts_receivable?.total.toLocaleString()}</span>
                    </div>
                    <div className="stat-row">
                        <span>Payables (AP):</span>
                        <span style={{ color: 'var(--danger)' }}>-${accounts_payable?.total.toLocaleString()}</span>
                    </div>
                    <div className="stat-row">
                        <span>Loans/Debt:</span>
                        <span style={{ color: 'var(--warning)' }}>-${loan_obligations?.total.toLocaleString()}</span>
                    </div>
                    <div className="stat-row">
                        <span>Tax Due:</span>
                        <span style={{ color: 'var(--danger)' }}>-${tax_compliance?.total.toLocaleString()}</span>
                    </div>
                </div>

                {/* Inventory */}
                <div className="card glass-card">
                    <h3>Inventory Status</h3>
                    <div className="risk-indicator" style={{ color: 'var(--text-main)', fontSize: '2rem' }}>
                        ${inventory_levels?.total.toLocaleString()}
                    </div>
                    <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                        Current value of stock on hand.
                    </p>
                </div>

            </div>

            <style>{`
                .stat-row {
                    display: flex;
                    justify-content: space-between;
                    padding: 0.8rem 0;
                    border-bottom: 1px solid var(--glass-border);
                }
                .stat-row:last-child {
                    border-bottom: none;
                }
            `}</style>
        </div>
    );
};

export default ReportView;

import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { syncBankAccount } from '../services/api';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const ReportView = ({ report }) => {
    if (!report) return null;

    const [bankingData, setBankingData] = useState(report.banking_data);

    const handleConnectBank = async (provider) => {
        try {
            const result = await syncBankAccount(provider, report.id);
            setBankingData(result.data);
            alert(`Successfully connected to ${provider}!`);
        } catch (error) {
            console.error(error);
            alert("Failed to connect banking provider.");
        }
    };

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
                    <h3>Industry</h3>
                    <div className="risk-indicator" style={{ color: 'var(--accent)', fontSize: '1.2rem' }}>
                        {report.industry || "General"}
                    </div>
                </div>
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
            {/* Banking Integration */}
            <div className="card glass-card wide" style={{ marginTop: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h3>Banking Integration</h3>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <button className="primary-btn" onClick={() => handleConnectBank('Plaid')} style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}>
                            Connect Plaid (Mock)
                        </button>
                        <button className="primary-btn" onClick={() => handleConnectBank('Stripe')} style={{ fontSize: '0.8rem', padding: '0.5rem 1rem', background: '#6366f1' }}>
                            Connect Stripe (Mock)
                        </button>
                    </div>
                </div>

                {bankingData ? (
                    <div>
                        <div className="stat-row">
                            <span>Provider:</span>
                            <span style={{ fontWeight: 'bold' }}>{bankingData.provider}</span>
                        </div>
                        <div className="stat-row">
                            <span>Account Balance:</span>
                            <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>${bankingData.balance?.toLocaleString()}</span>
                        </div>
                        <h4 style={{ marginTop: '1rem', marginBottom: '0.5rem' }}>Recent Transactions</h4>
                        <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                                <thead>
                                    <tr style={{ textAlign: 'left', color: 'var(--text-muted)' }}>
                                        <th style={{ padding: '0.5rem' }}>Date</th>
                                        <th style={{ padding: '0.5rem' }}>Description</th>
                                        <th style={{ padding: '0.5rem', textAlign: 'right' }}>Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {bankingData.transactions?.map((tx, i) => (
                                        <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                            <td style={{ padding: '0.5rem' }}>{tx.date}</td>
                                            <td style={{ padding: '0.5rem' }}>{tx.description}</td>
                                            <td style={{ padding: '0.5rem', textAlign: 'right', color: tx.amount < 0 ? 'var(--danger)' : 'var(--success)' }}>
                                                ${tx.amount.toLocaleString()}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                        No banking data connected. Click a button above to simulate API integration.
                    </p>
                )}
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

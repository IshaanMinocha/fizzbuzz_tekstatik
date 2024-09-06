// Charts.js
import React from 'react';
import {
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer
} from 'recharts';
import { vulnerabilities, fuzzResultData } from './data';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const Charts = () => {
  // Prepare data for Vulnerabilities Pie Chart
  const severityCount = vulnerabilities.reduce((acc, curr) => {
    acc[curr.severity] = (acc[curr.severity] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.keys(severityCount).map(severity => ({
    name: severity.charAt(0).toUpperCase() + severity.slice(1),
    value: severityCount[severity]
  }));

  // Prepare data for Fuzz Results Bar Chart
  const fuzzResultsCount = fuzzResultData.reduce((acc, curr) => {
    acc[curr.user] = (acc[curr.user] || 0) + 1;
    return acc;
  }, {});

  const barData = Object.keys(fuzzResultsCount).map(user => ({
    user,
    count: fuzzResultsCount[user]
  }));

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}>
      {/* Vulnerabilities Pie Chart */}
      <div style={{ width: '45%', minWidth: '300px', margin: '20px 0' }}>
        <h3>Vulnerabilities by Severity</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <RechartsTooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Fuzz Results Bar Chart */}
      <div style={{ width: '45%', minWidth: '300px', margin: '20px 0' }}>
        <h3>Fuzz Results per User</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={barData}
            margin={{
              top: 20, right: 30, left: 20, bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="user" />
            <YAxis allowDecimals={false} />
            <RechartsTooltip />
            <Legend />
            <Bar dataKey="count" fill="#82ca9d" name="Number of Fuzz Results" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;

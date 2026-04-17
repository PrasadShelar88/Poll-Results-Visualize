import { useMemo, useState } from 'react'
import Papa from 'papaparse'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  AreaChart,
  Area,
} from 'recharts'
import ChartCard from './components/ChartCard'
import StatCard from './components/StatCard'
import sampleCsv from './data/cleaned_poll_data.csv?raw'
import sampleInsights from './data/insights.json'
import {
  cleanRows,
  computeInsights,
  dailyTrend,
  feedbackKeywords,
  groupAverage,
  groupCounts,
  regionToolMatrix,
  toSeries,
} from './utils'

const PIE_COLORS = ['#6d5efc', '#19c37d', '#ffb020', '#ff6b6b', '#00b8d9', '#a855f7']

function parseSampleRows() {
  const { data } = Papa.parse(sampleCsv, { header: true, skipEmptyLines: true })
  return cleanRows(data)
}

const rawSampleRows = parseSampleRows()

export default function App() {
  const [rows, setRows] = useState(rawSampleRows)
  const [sourceName, setSourceName] = useState('Sample backend dataset')
  const [selectedRegion, setSelectedRegion] = useState('All')
  const [selectedAge, setSelectedAge] = useState('All')
  const [selectedTool, setSelectedTool] = useState('All')

  const regions = useMemo(() => ['All', ...new Set(rows.map((row) => row.Region))], [rows])
  const ageGroups = useMemo(() => ['All', ...new Set(rows.map((row) => row['Age Group']))], [rows])
  const tools = useMemo(() => ['All', ...new Set(rows.map((row) => row['Preferred Tool']))], [rows])

  const filteredRows = useMemo(() => {
    return rows.filter((row) => {
      const matchRegion = selectedRegion === 'All' || row.Region === selectedRegion
      const matchAge = selectedAge === 'All' || row['Age Group'] === selectedAge
      const matchTool = selectedTool === 'All' || row['Preferred Tool'] === selectedTool
      return matchRegion && matchAge && matchTool
    })
  }, [rows, selectedRegion, selectedAge, selectedTool])

  const insights = useMemo(() => computeInsights(filteredRows), [filteredRows])
  const toolSeries = useMemo(() => toSeries(groupCounts(filteredRows, 'Preferred Tool'), 'tool', 'votes'), [filteredRows])
  const regionSeries = useMemo(() => regionToolMatrix(filteredRows), [filteredRows])
  const dailySeries = useMemo(() => dailyTrend(filteredRows), [filteredRows])
  const ageSatisfactionSeries = useMemo(
    () => groupAverage(filteredRows, 'Age Group', 'Satisfaction (1-5)').map((item) => ({ ageGroup: item.name, satisfaction: item.value })),
    [filteredRows]
  )
  const keywordSeries = useMemo(() => feedbackKeywords(filteredRows), [filteredRows])

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    const text = await file.text()
    const { data } = Papa.parse(text, { header: true, skipEmptyLines: true })
    setRows(cleanRows(data))
    setSourceName(file.name)
    setSelectedRegion('All')
    setSelectedAge('All')
    setSelectedTool('All')
  }

  const resetToSample = () => {
    setRows(rawSampleRows)
    setSourceName('Sample backend dataset')
    setSelectedRegion('All')
    setSelectedAge('All')
    setSelectedTool('All')
  }

  const insightsHint = typeof sampleInsights === 'object' ? `Backend sample top tool: ${sampleInsights.top_tool}` : ''

  return (
    <div className="page-shell">
      <header className="hero-section">
        <div>
          <p className="eyebrow">Data Analyst Portfolio Project</p>
          <h1>Poll Results Visualizer</h1>
          <p className="hero-text">
            A polished frontend dashboard that matches your backend outputs and turns poll responses into charts,
            comparisons, and decision-ready insights.
          </p>
        </div>
        <div className="upload-panel">
          <span className="source-badge">Current source: {sourceName}</span>
          <label className="upload-button">
            Upload cleaned_poll_data.csv
            <input type="file" accept=".csv" onChange={handleFileUpload} hidden />
          </label>
          <button className="secondary-button" onClick={resetToSample}>Use sample backend data</button>
        </div>
      </header>

      <section className="filters-panel">
        <div>
          <label>Region</label>
          <select value={selectedRegion} onChange={(e) => setSelectedRegion(e.target.value)}>
            {regions.map((region) => <option key={region}>{region}</option>)}
          </select>
        </div>
        <div>
          <label>Age Group</label>
          <select value={selectedAge} onChange={(e) => setSelectedAge(e.target.value)}>
            {ageGroups.map((age) => <option key={age}>{age}</option>)}
          </select>
        </div>
        <div>
          <label>Preferred Tool</label>
          <select value={selectedTool} onChange={(e) => setSelectedTool(e.target.value)}>
            {tools.map((tool) => <option key={tool}>{tool}</option>)}
          </select>
        </div>
      </section>

      <section className="stats-grid">
        <StatCard label="Total Responses" value={insights.total_responses} hint="Filtered records shown on this dashboard" />
        <StatCard label="Top Tool" value={insights.top_tool} hint={insightsHint} />
        <StatCard label="Average Satisfaction" value={insights.average_satisfaction} hint="Based on the 1–5 satisfaction score" />
        <StatCard label="Top Share %" value={`${insights.top_share_percent}%`} hint="Vote share of the leading option" />
      </section>

      <section className="charts-grid two-col">
        <ChartCard title="Tool Preference" subtitle="Vote counts for each option in the filtered dataset">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={toolSeries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="tool" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="votes" radius={[10, 10, 0, 0]} fill="#6d5efc" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Vote Share" subtitle="Pie chart showing percentage distribution of preferences">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={toolSeries} dataKey="votes" nameKey="tool" outerRadius={110} innerRadius={55} paddingAngle={3}>
                {toolSeries.map((_, index) => <Cell key={index} fill={PIE_COLORS[index % PIE_COLORS.length]} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </section>

      <section className="charts-grid two-col">
        <ChartCard title="Responses Over Time" subtitle="Daily submission trend from the cleaned backend dataset">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dailySeries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="responses" stroke="#19c37d" strokeWidth={3} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Average Satisfaction by Age Group" subtitle="Compares satisfaction patterns across demographics">
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={ageSatisfactionSeries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ageGroup" />
              <YAxis domain={[0, 5]} />
              <Tooltip />
              <Area type="monotone" dataKey="satisfaction" stroke="#ffb020" fill="#ffdd9a" />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>
      </section>

      <section className="charts-grid two-col">
        <ChartCard title="Region vs Tool Comparison" subtitle="Stacked analysis for geographic preference segmentation">
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={regionSeries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              {tools.filter((tool) => tool !== 'All').map((tool, index) => (
                <Bar key={tool} dataKey={tool} stackId="a" fill={PIE_COLORS[index % PIE_COLORS.length]} radius={index === tools.length - 2 ? [6, 6, 0, 0] : 0} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Feedback Keywords" subtitle="Top repeated terms extracted from text responses">
          <div className="keyword-wrap">
            {keywordSeries.length ? keywordSeries.map((item) => (
              <div key={item.word} className="keyword-pill">
                <span>{item.word}</span>
                <strong>{item.count}</strong>
              </div>
            )) : <p className="empty-text">No feedback text available for the current filters.</p>}
          </div>
        </ChartCard>
      </section>

      <ChartCard title="Dataset Preview" subtitle="Useful for demo screenshots and project explanation">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Region</th>
                <th>Age Group</th>
                <th>Preferred Tool</th>
                <th>Satisfaction</th>
                <th>Feedback</th>
              </tr>
            </thead>
            <tbody>
              {filteredRows.slice(0, 8).map((row) => (
                <tr key={`${row.id}-${row.Timestamp}`}>
                  <td>{row.Timestamp}</td>
                  <td>{row.Region}</td>
                  <td>{row['Age Group']}</td>
                  <td>{row['Preferred Tool']}</td>
                  <td>{row['Satisfaction (1-5)']}</td>
                  <td>{row.Feedback || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ChartCard>
    </div>
  )
}

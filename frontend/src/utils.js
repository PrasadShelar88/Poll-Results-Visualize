import Papa from 'papaparse'

export function parseCSVText(text) {
  const { data } = Papa.parse(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (header) => header.trim()
  })
  return data
}

export function safeNumber(value) {
  const num = Number(value)
  return Number.isFinite(num) ? num : 0
}

export function titleCase(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\b\w/g, (m) => m.toUpperCase())
}

export function cleanRows(rows) {
  return rows
    .map((row, index) => {
      const timestamp = row.Timestamp || row.timestamp || ''
      const preferredTool = titleCase(row['Preferred Tool'] || row.preferred_tool || row.Tool)
      const ageGroup = row['Age Group'] || row.age_group || 'Unknown'
      const region = row.Region || row.region || 'Unknown'
      const satisfaction = safeNumber(row['Satisfaction (1-5)'] || row.Satisfaction || row.rating)
      const feedback = String(row.Feedback || row.feedback || '').trim()
      const date = timestamp ? new Date(timestamp).toISOString().slice(0, 10) : 'Unknown'
      return {
        id: row['Respondent ID'] || row.id || index + 1,
        Timestamp: timestamp,
        Date: date,
        Region: region,
        'Age Group': ageGroup,
        'Preferred Tool': preferredTool,
        'Satisfaction (1-5)': satisfaction,
        Feedback: feedback,
      }
    })
    .filter((row) => row['Preferred Tool'])
}

export function computeInsights(rows) {
  const totalResponses = rows.length
  const grouped = groupCounts(rows, 'Preferred Tool')
  const sortedTools = Object.entries(grouped).sort((a, b) => b[1] - a[1])
  const topTool = sortedTools[0]?.[0] || 'N/A'
  const topToolVotes = sortedTools[0]?.[1] || 0
  const avgSatisfaction = totalResponses
    ? (rows.reduce((sum, row) => sum + safeNumber(row['Satisfaction (1-5)']), 0) / totalResponses).toFixed(2)
    : '0.00'
  const topSharePercent = totalResponses ? ((topToolVotes / totalResponses) * 100).toFixed(2) : '0.00'

  return {
    total_responses: totalResponses,
    top_tool: topTool,
    average_satisfaction: avgSatisfaction,
    top_share_percent: topSharePercent,
  }
}

export function groupCounts(rows, column) {
  return rows.reduce((acc, row) => {
    const key = row[column] || 'Unknown'
    acc[key] = (acc[key] || 0) + 1
    return acc
  }, {})
}

export function groupAverage(rows, groupColumn, valueColumn) {
  const buckets = {}
  for (const row of rows) {
    const key = row[groupColumn] || 'Unknown'
    if (!buckets[key]) buckets[key] = { total: 0, count: 0 }
    buckets[key].total += safeNumber(row[valueColumn])
    buckets[key].count += 1
  }
  return Object.entries(buckets).map(([name, stats]) => ({
    name,
    value: Number((stats.total / stats.count).toFixed(2)),
  }))
}

export function toSeries(grouped, keyName = 'name', valueName = 'value') {
  return Object.entries(grouped).map(([key, value]) => ({ [keyName]: key, [valueName]: value }))
}

export function regionToolMatrix(rows) {
  const regions = [...new Set(rows.map((row) => row.Region))]
  const tools = [...new Set(rows.map((row) => row['Preferred Tool']))]
  return regions.map((region) => {
    const entry = { region }
    for (const tool of tools) entry[tool] = 0
    for (const row of rows) {
      if (row.Region === region) entry[row['Preferred Tool']] += 1
    }
    return entry
  })
}

export function dailyTrend(rows) {
  const grouped = groupCounts(rows, 'Date')
  return Object.entries(grouped)
    .map(([date, responses]) => ({ date, responses }))
    .sort((a, b) => a.date.localeCompare(b.date))
}

export function feedbackKeywords(rows, limit = 12) {
  const stopWords = new Set(['the', 'and', 'for', 'with', 'this', 'that', 'have', 'from', 'very', 'more', 'need', 'good', 'great', 'tool'])
  const counts = {}
  for (const row of rows) {
    const words = String(row.Feedback || '')
      .toLowerCase()
      .replace(/[^a-z\s]/g, ' ')
      .split(/\s+/)
      .filter((word) => word.length > 2 && !stopWords.has(word))
    for (const word of words) counts[word] = (counts[word] || 0) + 1
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([word, count]) => ({ word, count }))
}

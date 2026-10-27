import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Label, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api, { errText } from '../api';

const Chart = ({ title, data, k, v, xl, yl, h }) => (
  <div className="card"><h3>{title}</h3><div style={{ height: 300 }}><ResponsiveContainer>
    <BarChart data={data} layout={h ? 'vertical' : 'horizontal'} margin={{ left: 10, bottom: 24 }}>
      <CartesianGrid strokeDasharray="3 3" />
      {h ? [<XAxis key="x" type="number"><Label value={xl} position="insideBottom" offset={-12} /></XAxis>,
            <YAxis key="y" type="category" dataKey={k} width={130} />]
         : [<XAxis key="x" dataKey={k}><Label value={xl} position="insideBottom" offset={-12} /></XAxis>,
            <YAxis key="y"><Label value={yl} angle={-90} position="insideLeft" /></YAxis>]}
      <Tooltip /><Bar dataKey={v} fill="#9b2a4a" /></BarChart></ResponsiveContainer></div></div>);

export default function Analysis() {
  const [a, setA] = useState(null), [err, setErr] = useState('');
  useEffect(() => { api.get('/analysis/').then(r => setA(r.data)).catch(e => setErr(errText(e))); }, []);
  if (err) return <main><div className="msg err">{err}</div></main>;
  if (!a) return <main>Loading…</main>;
  const s = a.summary;
  const cards = [['Total samples', s.samples], ['Average quality', s.mean_quality], ['Most frequent score', s.mode_quality],
    ['Chemical features', s.features], ['Missing values', s.missing], ['Duplicate rows', s.duplicates]];
  return (<main><h2>Overview &amp; Quality Analysis</h2>
    <div className="grid">{cards.map(([l, v]) => <div className="card stat" key={l}><b>{v}</b><span>{l}</span></div>)}</div>
    <div className="msg">{a.text}</div>
    <div className="grid">
      <Chart title="Quality score distribution" data={a.quality_distribution} k="quality" v="count" xl="Quality score" yl="Samples" />
      <Chart title="Alcohol distribution" data={a.alcohol_histogram} k="bin" v="count" xl="Alcohol (% vol, bin start)" yl="Samples" />
      <Chart title="Mean alcohol by quality" data={a.alcohol_by_quality} k="quality" v="mean_alcohol" xl="Quality score" yl="Mean alcohol (% vol)" />
      <Chart title="Correlation with quality" data={a.correlations} k="feature" v="r" xl="Pearson r" h />
    </div>
    <div className="card wrap"><h3>Descriptive statistics</h3><table><thead><tr>{Object.keys(a.stats[0]).map(c => <th key={c}>{c}</th>)}</tr></thead>
      <tbody>{a.stats.map(r => <tr key={r.column}>{Object.values(r).map((v, i) => <td key={i} style={i ? {} : { textAlign: 'left' }}>{v}</td>)}</tr>)}</tbody></table></div>
    <div className="msg"><b>Caveat:</b> correlation shows linear association only, not what causes quality. Quality is an ordinal expert score (0–10), not a percentage.</div>
  </main>);
}

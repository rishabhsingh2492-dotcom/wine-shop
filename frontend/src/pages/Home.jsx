import { Link } from 'react-router-dom';
const feats = [['/explorer', 'Explore Dataset', 'View and filter wine data with ease.'],
  ['/analysis', 'Visualize Insights', 'Interactive charts and statistical analysis.'],
  ['/analysis', 'Analyze Quality', 'Understand key factors and correlations.'],
  ['/predict', 'Predict Quality', 'Estimate quality from chemical properties.'],
  ['/explorer', 'Download Reports', 'Export filtered data in CSV format.']];
export default function Home() {
  return (<>
    <section className="hero"><small>DATA · ANALYSIS · INSIGHTS</small>
      <h1>Wine Quality Analysis <span>Made Simple</span></h1>
      <p>Explore, analyze and understand wine quality data through interactive visualizations and insights, backed by real data.</p>
      <Link className="btn" to="/explorer">Explore Dataset →</Link></section>
    <main><div className="grid">{feats.map(([to, t, d]) => (
      <Link key={t} to={to} style={{ textDecoration: 'none', color: 'inherit' }}>
        <div className="card"><h3>{t}</h3><span style={{ color: 'var(--mut)' }}>{d}</span></div></Link>))}</div></main>
  </>);
}

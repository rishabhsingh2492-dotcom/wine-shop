import { useEffect, useState } from 'react';
import api, { errText } from '../api';

const F = [['fixed_acidity', 'Fixed acidity', 'g/dm³'], ['volatile_acidity', 'Volatile acidity', 'g/dm³'],
  ['citric_acid', 'Citric acid', 'g/dm³'], ['residual_sugar', 'Residual sugar', 'g/dm³'], ['chlorides', 'Chlorides', 'g/dm³'],
  ['free_sulfur_dioxide', 'Free sulfur dioxide', 'mg/dm³'], ['total_sulfur_dioxide', 'Total sulfur dioxide', 'mg/dm³'],
  ['density', 'Density', 'g/cm³'], ['ph', 'pH', '0–14'], ['sulphates', 'Sulphates', 'g/dm³'], ['alcohol', 'Alcohol', '% vol']];

export default function Predict() {
  const [v, setV] = useState({}), [bad, setBad] = useState({}), [res, setRes] = useState(null), [err, setErr] = useState('');
  const [hist, setHist] = useState([]), [medians, setMedians] = useState(null);
  const loadHist = () => api.get('/predictions/').then(r => setHist(r.data)).catch(() => {});
  useEffect(() => {
    loadHist();
    api.get('/analysis/').then(r => setMedians(Object.fromEntries(r.data.stats.map(s => [s.column, s.median])))).catch(() => {});
  }, []);
  const submit = async e => {
    e.preventDefault(); setErr(''); setRes(null);
    const b = {}; F.forEach(([k]) => { const n = Number(v[k]); if (v[k] === undefined || v[k] === '' || !Number.isFinite(n) || n < 0) b[k] = 'Enter a finite, non-negative number.'; });
    setBad(b); if (Object.keys(b).length) return;
    try { setRes((await api.post('/predict/', Object.fromEntries(F.map(([k]) => [k, Number(v[k])])))).data); loadHist(); }
    catch (x) { setErr(x.response?.data?.errors ? 'Server rejected some values.' : errText(x)); }
  };
  return (<main><h2>Predict Quality</h2>
    <div className="msg">Predictions come from a RandomForest model trained separately (<code>python manage.py train_wine_model</code>). They are estimates, not laboratory measurements.</div>
    <form className="card" onSubmit={submit} noValidate><div className="f">{F.map(([k, l, u]) => (
      <div key={k}><label htmlFor={k}>{l}</label><input id={k} inputMode="decimal" value={v[k] ?? ''} onChange={e => setV({ ...v, [k]: e.target.value })} />
        <small>{u}</small><div className="bad">{bad[k]}</div></div>))}</div>
      <div className="bar"><button className="btn">Predict Quality</button>
        <button type="button" className="btn alt" disabled={!medians} onClick={() => setV(medians)}>Load example (dataset medians)</button>
        <button type="button" className="btn alt" onClick={() => { setV({}); setBad({}); setRes(null); }}>Reset</button></div></form>
    {err && <div className="msg err">{err}</div>}
    {res && <div className="card ok" style={{ marginTop: 16 }}><h3>Predicted quality score: {res.predicted_score} / 10</h3>
      <div className="scale">{[...Array(11).keys()].map(i => <i key={i} className={i === res.predicted_score ? 'on' : ''}>{i}</i>)}</div>
      <p>Raw model output {res.predicted_raw}, rounded to the nearest integer and clipped to 0–10. Model: {res.model}. {new Date(res.created_at).toLocaleString()}</p>
      <p>Held-out test metrics: MAE {res.metrics.mae}, RMSE {res.metrics.rmse}, R² {res.metrics.r2}. {res.note}</p></div>}
    <h3 style={{ marginTop: 24 }}>Prediction history</h3>
    {!hist.length ? <div className="msg">No predictions yet.</div> : <div className="card wrap"><table><thead><tr><th>ID</th><th>Score</th><th>Raw</th><th>Model</th><th>Time</th></tr></thead>
      <tbody>{hist.map(p => <tr key={p.id}><td>{p.id}</td><td>{p.predicted_score}</td><td>{p.predicted_raw}</td><td>{p.model}</td><td>{new Date(p.created_at).toLocaleString()}</td></tr>)}</tbody></table></div>}
  </main>);
}

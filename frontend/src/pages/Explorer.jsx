import { useEffect, useState } from 'react';
import api, { BASE, errText } from '../api';

export default function Explorer() {
  const [p, setP] = useState({ page: 1, quality: '', min_alcohol: '', max_alcohol: '', search: '', sort: 'id' });
  const [d, setD] = useState(null), [err, setErr] = useState('');
  const params = Object.fromEntries(Object.entries(p).filter(([, v]) => v !== ''));
  useEffect(() => { setErr(''); api.get('/dataset/', { params }).then(r => setD(r.data)).catch(e => setErr(errText(e))); },
    [JSON.stringify(params)]);
  const set = (k, v) => setP({ ...p, [k]: v, page: 1 });
  const sortBy = c => set('sort', p.sort === c ? '-' + c : c);
  const cols = d?.results[0] ? Object.keys(d.results[0]).filter(c => c !== 'id') : [];
  const qs = new URLSearchParams({ ...params, page: undefined }); qs.delete('page');
  return (<main><h2>Dataset Explorer</h2>
    <div className="bar">
      <div><label>Search (numeric)</label><input value={p.search} onChange={e => set('search', e.target.value)} /></div>
      <div><label>Quality</label><select value={p.quality} onChange={e => set('quality', e.target.value)}>
        <option value="">All</option>{[3, 4, 5, 6, 7, 8].map(q => <option key={q}>{q}</option>)}</select></div>
      <div><label>Min alcohol</label><input type="number" value={p.min_alcohol} onChange={e => set('min_alcohol', e.target.value)} /></div>
      <div><label>Max alcohol</label><input type="number" value={p.max_alcohol} onChange={e => set('max_alcohol', e.target.value)} /></div>
      <a className="btn alt" href={`${BASE}/export/?${qs}`}>Export filtered CSV</a></div>
    {err && <div className="msg err">{err}</div>}
    {d && <p>{d.count} matching records</p>}
    {d && d.count === 0 && <div className="msg">No rows match these filters.</div>}
    {d && d.count > 0 && <div className="card wrap"><table><thead><tr>{cols.map(c =>
      <th key={c} onClick={() => sortBy(c)}>{c.replace(/_/g, ' ')}{p.sort === c ? ' ▲' : p.sort === '-' + c ? ' ▼' : ''}</th>)}</tr></thead>
      <tbody>{d.results.map(r => <tr key={r.id}>{cols.map(c => <td key={c}>{r[c]}</td>)}</tr>)}</tbody></table></div>}
    {d && <div className="bar"><button className="btn alt" disabled={d.page <= 1} onClick={() => setP({ ...p, page: p.page - 1 })}>‹ Prev</button>
      <span>Page {d.page} of {d.pages}</span>
      <button className="btn alt" disabled={d.page >= d.pages} onClick={() => setP({ ...p, page: p.page + 1 })}>Next ›</button></div>}
  </main>);
}

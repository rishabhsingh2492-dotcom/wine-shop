import { useEffect, useState } from 'react';
import { NavLink, Route, Routes, Link } from 'react-router-dom';
import api from './api';
import Home from './pages/Home';
import Explorer from './pages/Explorer';
import Analysis from './pages/Analysis';
import Predict from './pages/Predict';
import About from './pages/About';

const links = [['/', 'Home'], ['/explorer', 'Dataset Explorer'], ['/analysis', 'Analysis'],
  ['/predict', 'Predict Quality'], ['/about', 'About']];

export default function App() {
  const [h, setH] = useState(null);
  useEffect(() => { api.get('/health/').then(r => setH(r.data)).catch(() => setH(false)); }, []);
  const status = h === null ? 'Checking API…' : h === false ? 'API offline'
    : h.dataset_ready ? `Dataset: ${h.samples} samples` : 'Dataset not imported';
  return (<>
    <header>
      <Link className="logo" to="/">🍷 WineIQ</Link>
      <nav>{links.map(([to, t]) => <NavLink key={to} to={to} end={to === '/'}>{t}</NavLink>)}</nav>
      <span className="pill">{status}</span>
    </header>
    <Routes>
      <Route path="/" element={<Home />} /><Route path="/explorer" element={<Explorer />} />
      <Route path="/analysis" element={<Analysis />} /><Route path="/predict" element={<Predict />} />
      <Route path="/about" element={<About />} />
    </Routes>
  </>);
}

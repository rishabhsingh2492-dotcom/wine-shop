export default function About() {
  return (<main><h2>About Project</h2><div className="card">
    <p><b>WineIQ — Wine Quality Analysis &amp; Prediction System</b>: a B.Tech CSE (AI/ML) mini project to explore the physicochemical properties of red wine and relate them to sensory quality scores.</p>
    <p><b>Dataset:</b> P. Cortez, A. Cerdeira, F. Almeida, T. Matos, J. Reis, <i>Wine Quality</i>, UCI Machine Learning Repository (1,599 red samples, 11 features, target <code>quality</code>). <a href="https://archive.ics.uci.edu/dataset/186/wine+quality" target="_blank" rel="noreferrer">Source</a></p>
    <p><b>Architecture:</b> React (Vite) → Django REST API → Pandas analysis / scikit-learn model (Joblib) → PostgreSQL.</p>
    <p><b>Statistics vs prediction:</b> the Analysis page is descriptive statistics; the Predict page uses a separately trained model.</p>
    <p><b>Limitations:</b> red wine only, subjective expert scores, correlation is not causation, quality is a discrete ordinal score, no authentication (local demo only).</p></div></main>);
}

import { usePyodide } from './hooks/usePyodide';
import Terminal from './components/Terminal';
import './App.css';

function App() {
  const { pyodide, loading, error, runPython } = usePyodide();

  if (loading) {
    return (
      <div className="loading">
        <p>Loading Python environment...</p>
        <p style={{fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7}}>
          ~10 seconds on first load
        </p>
      </div>
    );
  }

  if (error) {
    return <div className="error">Failed to load: {error}</div>;
  }

  return <Terminal runPython={runPython} />;
}

export default App;
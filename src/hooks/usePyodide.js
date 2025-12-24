import { useEffect, useState } from 'react';

export const usePyodide = () => {
  const [pyodide, setPyodide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPyodide = async () => {
      try {
        // Wait for window.loadPyodide to be available
        while (!window.loadPyodide) {
          await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        const pyodideModule = await window.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
        });
        
        const response = await fetch('/linalg.py');
        const pythonCode = await response.text();
        await pyodideModule.runPythonAsync(pythonCode);
        
        setPyodide(pyodideModule);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    loadPyodide();
  }, []);

  const runPython = async (code) => {
    if (!pyodide) return { error: 'Pyodide not loaded' };
    
    try {
      const result = await pyodide.runPythonAsync(code);
      return { result };
    } catch (err) {
      return { error: parseError(err.message) };
    }
  };

  return { pyodide, loading, error, runPython };
};

const parseError = (message) => {
  if (message.includes('ValueError')) {
    return message.split('ValueError: ')[1] || 'Invalid input';
  }
  if (message.includes('NameError')) {
    return 'Variable not found';
  }
  if (message.includes('TypeError')) {
    return 'Type error - check your input format';
  }
  return 'Error: ' + message.split('\n')[0];
};
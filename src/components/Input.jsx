import { useState } from 'react';
import './Input.css';

function Input({ onSubmit, onClear, commandHistory, historyIndex, setHistoryIndex }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    // Up arrow - navigate back in history
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (commandHistory.length > 0) {
        const newIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setInput(commandHistory[newIndex]);
      }
    }
    
    // Down arrow - navigate forward in history
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex === -1) return;
      
      const newIndex = historyIndex + 1;
      if (newIndex >= commandHistory.length) {
        setHistoryIndex(-1);
        setInput('');
      } else {
        setHistoryIndex(newIndex);
        setInput(commandHistory[newIndex]);
      }
    }

    // Ctrl+L - clear terminal
    if (e.ctrlKey && e.key === 'l') {
      e.preventDefault();
      onClear();
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="input-form">
      <span className="prompt">{'>>>'}</span>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        className="input-field"
        autoFocus
        spellCheck={false}
        autoComplete="off"
      />
    </form>
  );
}

export default Input;
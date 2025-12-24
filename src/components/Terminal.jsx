import { useState, useRef, useEffect } from 'react';
import Input from './Input';
import Output from './Output';
import { parseCommand, executeCommand } from '../utils/parser.js';
import './Terminal.css';

function Terminal({ runPython }) {
  const [history, setHistory] = useState([]);
  const [workspace, setWorkspace] = useState({});
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [promptState, setPromptState] = useState(null); // For interactive prompts
  const terminalContentRef = useRef(null);

  useEffect(() => {
    if (terminalContentRef.current) {
      // Use requestAnimationFrame twice to ensure DOM has fully updated
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          if (terminalContentRef.current) {
            terminalContentRef.current.scrollTop = terminalContentRef.current.scrollHeight;
          }
        });
      });
    }
  }, [history]);

  const handleCommand = async (input) => {
    if (!input.trim()) return;

    // If we're in a prompt state, handle the prompt response
    if (promptState) {
      handlePromptResponse(input);
      return;
    }

    // Add to command history
    setCommandHistory(prev => [...prev, input]);
    setHistoryIndex(-1);

    // Add input to display history
    setHistory(prev => [...prev, { type: 'input', content: input }]);

    // Parse and execute
    const parsed = parseCommand(input, workspace);

    if (parsed.error) {
      setHistory(prev => [...prev, { type: 'error', content: parsed.error }]);
      return;
    }

    // Handle clear command
    if (parsed.type === 'clear') {
      setHistory([]);
      return;
    }

    // Handle interactive function calls and interactive assignments
    if (parsed.type === 'interactive_function' || parsed.type === 'interactive_assign_function' || parsed.type === 'interactive_assign') {
      startInteractivePrompt(parsed);
      return;
    }

    const result = await executeCommand(parsed, runPython, workspace);

    if (result.workspace) {
      setWorkspace(result.workspace);
    }

    if (result.content !== undefined && result.content !== '') {
      setHistory(prev => [...prev, {
        type: result.error ? 'error' : 'output',
        content: result.content
      }]);
    }
  };

  const startInteractivePrompt = (parsed) => {
    const { funcName, inputType, varName, type } = parsed;

    // Initialize prompt state
    const state = {
      funcName,
      inputType,
      varName, // For assignments
      isDirectAssign: type === 'interactive_assign', // Flag for direct matrix/vector assignment
      step: 0,
      collectedData: {}
    };

    setPromptState(state);

    // Show the first prompt
    const firstPrompt = getNextPrompt(state);
    setHistory(prev => [...prev, { type: 'prompt', content: firstPrompt }]);
  };

  const getNextPrompt = (state) => {
    const { inputType, step, collectedData } = state;

    if (inputType === 'matrix') {
      if (step === 0) return 'Number of rows:';
      if (step === 1) return 'Number of columns:';
      if (step >= 2) {
        const rowNum = step - 2;
        const totalRows = collectedData.rows;
        if (rowNum < totalRows) {
          return `Row ${rowNum + 1} (space-separated):`;
        }
      }
    } else if (inputType === 'vector') {
      return 'Vector (space-separated values):';
    } else if (inputType === 'two_vectors') {
      if (step === 0) return 'Vector 1 (space-separated values):';
      if (step === 1) return 'Vector 2 (space-separated values):';
    } else if (inputType === 'two_matrices') {
      if (!collectedData.matrix1) {
        if (step === 0) return 'Matrix 1 - Number of rows:';
        if (step === 1) return 'Matrix 1 - Number of columns:';
        if (step >= 2) {
          const rowNum = step - 2;
          const totalRows = collectedData.rows1;
          if (rowNum < totalRows) {
            return `Matrix 1 - Row ${rowNum + 1} (space-separated):`;
          }
        }
      } else {
        const baseStep = 2 + collectedData.rows1;
        if (step === baseStep) return 'Matrix 2 - Number of rows:';
        if (step === baseStep + 1) return 'Matrix 2 - Number of columns:';
        if (step >= baseStep + 2) {
          const rowNum = step - baseStep - 2;
          const totalRows = collectedData.rows2;
          if (rowNum < totalRows) {
            return `Matrix 2 - Row ${rowNum + 1} (space-separated):`;
          }
        }
      }
    } else if (inputType === 'matrix_vector') {
      if (!collectedData.vector) {
        return 'Vector (space-separated values):';
      } else {
        if (step === 1) return 'Matrix - Number of rows:';
        if (step === 2) return 'Matrix - Number of columns:';
        if (step >= 3) {
          const rowNum = step - 3;
          const totalRows = collectedData.rows;
          if (rowNum < totalRows) {
            return `Matrix - Row ${rowNum + 1} (space-separated):`;
          }
        }
      }
    }

    return null;
  };

  const handlePromptResponse = async (input) => {
    const state = { ...promptState };
    const { inputType, step, collectedData } = state;

    // Add the user's response to history
    setHistory(prev => [...prev, { type: 'input', content: input }]);

    try {
      if (inputType === 'matrix') {
        if (step === 0) {
          collectedData.rows = parseInt(input);
          if (isNaN(collectedData.rows) || collectedData.rows <= 0) {
            throw new Error('Invalid number of rows');
          }
        } else if (step === 1) {
          collectedData.cols = parseInt(input);
          if (isNaN(collectedData.cols) || collectedData.cols <= 0) {
            throw new Error('Invalid number of columns');
          }
          collectedData.matrix = [];
        } else {
          const rowData = input.trim().split(/\s+/).map(Number);
          if (rowData.length !== collectedData.cols || rowData.some(isNaN)) {
            throw new Error(`Expected ${collectedData.cols} numbers`);
          }
          collectedData.matrix.push(rowData);
        }
      } else if (inputType === 'vector') {
        const vectorData = input.trim().split(/\s+/).map(Number);
        if (vectorData.some(isNaN)) {
          throw new Error('Invalid vector values');
        }
        collectedData.vector = vectorData;
      } else if (inputType === 'two_vectors') {
        const vectorData = input.trim().split(/\s+/).map(Number);
        if (vectorData.some(isNaN)) {
          throw new Error('Invalid vector values');
        }
        if (step === 0) {
          collectedData.vector1 = vectorData;
        } else {
          collectedData.vector2 = vectorData;
        }
      } else if (inputType === 'two_matrices') {
        if (!collectedData.matrix1) {
          if (step === 0) {
            collectedData.rows1 = parseInt(input);
            if (isNaN(collectedData.rows1) || collectedData.rows1 <= 0) {
              throw new Error('Invalid number of rows');
            }
          } else if (step === 1) {
            collectedData.cols1 = parseInt(input);
            if (isNaN(collectedData.cols1) || collectedData.cols1 <= 0) {
              throw new Error('Invalid number of columns');
            }
            collectedData.matrix1 = [];
          } else {
            const rowData = input.trim().split(/\s+/).map(Number);
            if (rowData.length !== collectedData.cols1 || rowData.some(isNaN)) {
              throw new Error(`Expected ${collectedData.cols1} numbers`);
            }
            collectedData.matrix1.push(rowData);
          }
        } else {
          const baseStep = 2 + collectedData.rows1;
          if (step === baseStep) {
            collectedData.rows2 = parseInt(input);
            if (isNaN(collectedData.rows2) || collectedData.rows2 <= 0) {
              throw new Error('Invalid number of rows');
            }
          } else if (step === baseStep + 1) {
            collectedData.cols2 = parseInt(input);
            if (isNaN(collectedData.cols2) || collectedData.cols2 <= 0) {
              throw new Error('Invalid number of columns');
            }
            collectedData.matrix2 = [];
          } else {
            const rowData = input.trim().split(/\s+/).map(Number);
            if (rowData.length !== collectedData.cols2 || rowData.some(isNaN)) {
              throw new Error(`Expected ${collectedData.cols2} numbers`);
            }
            collectedData.matrix2.push(rowData);
          }
        }
      } else if (inputType === 'matrix_vector') {
        if (!collectedData.vector) {
          const vectorData = input.trim().split(/\s+/).map(Number);
          if (vectorData.some(isNaN)) {
            throw new Error('Invalid vector values');
          }
          collectedData.vector = vectorData;
        } else {
          if (step === 1) {
            collectedData.rows = parseInt(input);
            if (isNaN(collectedData.rows) || collectedData.rows <= 0) {
              throw new Error('Invalid number of rows');
            }
          } else if (step === 2) {
            collectedData.cols = parseInt(input);
            if (isNaN(collectedData.cols) || collectedData.cols <= 0) {
              throw new Error('Invalid number of columns');
            }
            collectedData.matrix = [];
          } else {
            const rowData = input.trim().split(/\s+/).map(Number);
            if (rowData.length !== collectedData.cols || rowData.some(isNaN)) {
              throw new Error(`Expected ${collectedData.cols} numbers`);
            }
            collectedData.matrix.push(rowData);
          }
        }
      }

      state.step++;
      state.collectedData = collectedData;

      // Check if we're done collecting input
      const isDone = checkIfPromptComplete(state);

      if (isDone) {
        // Execute the function with collected data
        await executeInteractiveFunction(state);
        setPromptState(null);
      } else {
        // Show next prompt
        const nextPrompt = getNextPrompt(state);
        setHistory(prev => [...prev, { type: 'prompt', content: nextPrompt }]);
        setPromptState(state);
      }
    } catch (error) {
      setHistory(prev => [...prev, { type: 'error', content: error.message }]);
      setPromptState(null);
    }
  };

  const checkIfPromptComplete = (state) => {
    const { inputType, collectedData } = state;

    if (inputType === 'matrix') {
      return collectedData.matrix && collectedData.matrix.length === collectedData.rows;
    } else if (inputType === 'vector') {
      return !!collectedData.vector;
    } else if (inputType === 'two_vectors') {
      return !!collectedData.vector1 && !!collectedData.vector2;
    } else if (inputType === 'two_matrices') {
      return collectedData.matrix1 && collectedData.matrix1.length === collectedData.rows1 &&
             collectedData.matrix2 && collectedData.matrix2.length === collectedData.rows2;
    } else if (inputType === 'matrix_vector') {
      return collectedData.vector && collectedData.matrix && collectedData.matrix.length === collectedData.rows;
    }

    return false;
  };

  const executeInteractiveFunction = async (state) => {
    const { funcName, inputType, collectedData, varName, isDirectAssign } = state;

    // If this is a direct assignment (matrix A / vector v), just store the value
    if (isDirectAssign) {
      let value;
      if (inputType === 'matrix') {
        value = collectedData.matrix;
      } else if (inputType === 'vector') {
        value = collectedData.vector;
      }

      const newWorkspace = { ...workspace, [varName]: value };
      setWorkspace(newWorkspace);
      setHistory(prev => [...prev, {
        type: 'output',
        content: `Stored ${varName}`
      }]);
      return;
    }

    // Build the parsed command based on collected data
    let args = [];

    if (inputType === 'matrix') {
      args = [JSON.stringify(collectedData.matrix)];
    } else if (inputType === 'vector') {
      args = [JSON.stringify(collectedData.vector)];
    } else if (inputType === 'two_vectors') {
      args = [JSON.stringify(collectedData.vector1), JSON.stringify(collectedData.vector2)];
    } else if (inputType === 'two_matrices') {
      args = [JSON.stringify(collectedData.matrix1), JSON.stringify(collectedData.matrix2)];
    } else if (inputType === 'matrix_vector') {
      args = [JSON.stringify(collectedData.matrix), JSON.stringify(collectedData.vector)];
    }

    const parsed = varName
      ? { type: 'assign_function', varName, funcName, args }
      : { type: 'function', funcName, args };

    console.log('executeInteractiveFunction parsed:', parsed);
    const result = await executeCommand(parsed, runPython, workspace);
    console.log('executeInteractiveFunction result:', result);

    if (result.workspace) {
      setWorkspace(result.workspace);
    }

    if (result.content !== undefined && result.content !== '') {
      console.log('Adding to history:', result.content);
      setHistory(prev => [...prev, {
        type: result.error ? 'error' : 'output',
        content: result.content
      }]);
    } else {
      console.log('Result content is empty or undefined:', result.content);
    }
  };

  const handleClear = () => {
    setHistory([]);
  };

  return (
    <div className="terminal-wrapper">
      <div className="terminal-header">
        <div className="terminal-header-left">
          <div className="terminal-title">row reducer</div>
          <div className="terminal-subtitle">Type 'help' to get started</div>
        </div>
        <div className="terminal-header-right">
          <div>↑/↓ - Command history</div>
          <div>Ctrl+L - Clear terminal</div>
        </div>
      </div>
      <div className="terminal">
        <div className="terminal-content" ref={terminalContentRef}>
          {history.map((item, idx) => (
            <Output key={idx} type={item.type} content={item.content} />
          ))}
        </div>
        <Input
          onSubmit={handleCommand}
          onClear={handleClear}
          commandHistory={commandHistory}
          historyIndex={historyIndex}
          setHistoryIndex={setHistoryIndex}
        />
      </div>
    </div>
  );
}

export default Terminal;
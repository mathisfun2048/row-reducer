import './Output.css';

function Output({ type, content }) {
  // Syntax highlighting for input lines
  const highlightSyntax = (text) => {
    const parts = [];
    let lastIndex = 0;

    // Match function names like: det(, rref(, trace(
    const functionRegex = /\b([a-z_][a-z0-9_]*)\s*\(/g;
    // Match variable names (single capital letters or lowercase single letters not followed by parenthesis)
    const variableRegex = /\b([A-Z][a-z0-9_]*|[a-z])(?!\s*\()/g;

    // Collect all matches with their positions and types
    const matches = [];

    let match;
    while ((match = functionRegex.exec(text)) !== null) {
      matches.push({
        start: match.index,
        end: match.index + match[1].length,
        text: match[1],
        type: 'function'
      });
    }

    while ((match = variableRegex.exec(text)) !== null) {
      // Check if this overlaps with a function match
      const overlaps = matches.some(m =>
        match.index >= m.start && match.index < m.end
      );
      if (!overlaps) {
        matches.push({
          start: match.index,
          end: match.index + match[1].length,
          text: match[1],
          type: 'variable'
        });
      }
    }

    // Sort by position
    matches.sort((a, b) => a.start - b.start);

    // Build the highlighted output
    matches.forEach((m, idx) => {
      // Add text before this match
      if (m.start > lastIndex) {
        parts.push(text.substring(lastIndex, m.start));
      }

      // Add highlighted match
      parts.push(
        <span key={idx} className={`syntax-${m.type}`}>
          {m.text}
        </span>
      );

      lastIndex = m.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }

    return parts.length > 0 ? parts : text;
  };

  const formatMatrix = (matrix) => {
    if (!Array.isArray(matrix)) return String(matrix);
    
    if (Array.isArray(matrix[0])) {
      // 2D matrix
      return matrix.map(row => 
        '[' + row.map(val => typeof val === 'number' ? val.toFixed(6) : val).join(', ') + ']'
      ).join('\n');
    } else {
      // 1D vector
      return '[' + matrix.map(val => typeof val === 'number' ? val.toFixed(6) : val).join(', ') + ']';
    }
  };

  const formatContent = () => {
    // Handle labeled results from parser
    if (typeof content === 'object' && content !== null && 'label' in content && 'value' in content) {
      const { label, parts, value } = content;

      // Handle multi-part outputs (LU, QR, diagonalize)
      if (parts && Array.isArray(value)) {
        let output = label ? `${label}\n` : '';
        if (value.length === 2 && Array.isArray(value[0]) && Array.isArray(value[1])) {
          // Two matrices
          output += `${parts[0]}\n${formatMatrix(value[0])}\n\n${parts[1]}\n${formatMatrix(value[1])}`;
        } else if (value.length === 3 && Array.isArray(value[0]) && Array.isArray(value[1]) && Array.isArray(value[2])) {
          // Three matrices
          output += `${parts[0]}\n${formatMatrix(value[0])}\n\n${parts[1]}\n${formatMatrix(value[1])}\n\n${parts[2]}\n${formatMatrix(value[2])}`;
        }
        return output;
      }

      // Handle eigenvectors special case
      if (label === 'Eigenvectors' && Array.isArray(value)) {
        if (value.length > 0 && Array.isArray(value[0]) && value[0].length === 2 && typeof value[0][0] === 'number') {
          return `${label}\n` + value.map((pair, idx) =>
            `Eigenvalue ${idx + 1}: ${pair[0].toFixed(6)}\nEigenvectors:\n${formatMatrix(pair[1])}`
          ).join('\n\n');
        }
      }

      // Handle regular labeled output
      if (label) {
        if (typeof value === 'number') {
          return `${label} ${value.toFixed(6)}`;
        }
        if (typeof value === 'boolean') {
          return `${label} ${String(value)}`;
        }
        if (Array.isArray(value)) {
          return `${label}\n${formatMatrix(value)}`;
        }
        return `${label} ${String(value)}`;
      }

      // Fallback to just the value
      return formatValue(value);
    }

    // Handle unlabeled content
    return formatValue(content);
  };

  const formatValue = (val) => {
    if (typeof val === 'string') {
      return val;
    }
    if (typeof val === 'number') {
      return val.toFixed(6);
    }
    if (typeof val === 'boolean') {
      return String(val);
    }
    if (Array.isArray(val)) {
      // Check if it's a tuple-like array (e.g., [L, U] or [Q, R])
      if (val.length === 2 && Array.isArray(val[0]) && Array.isArray(val[1])) {
        // Could be LU/QR (two matrices) or eigenvectors output (eigenvalue, vectors)
        if (typeof val[0] === 'number') {
          // eigenvectors: [eigenvalue, [vectors]]
          return `Eigenvalue: ${val[0].toFixed(6)}\nEigenvectors:\n${formatMatrix(val[1])}`;
        }
        // Two matrices (LU, QR)
        return formatMatrix(val[0]) + '\n\n' + formatMatrix(val[1]);
      }
      if (val.length === 3 && Array.isArray(val[0]) && Array.isArray(val[1]) && Array.isArray(val[2])) {
        // Three matrices (diagonalize: P, D, P_inv)
        return formatMatrix(val[0]) + '\n\n' + formatMatrix(val[1]) + '\n\n' + formatMatrix(val[2]);
      }
      // Check if it's a list of eigenvalue-eigenvector pairs
      if (val.length > 0 && Array.isArray(val[0]) && val[0].length === 2 && typeof val[0][0] === 'number') {
        // eigenvectors output: [[eigenvalue, [vectors]], ...]
        return val.map((pair, idx) =>
          `Eigenvalue ${idx + 1}: ${pair[0].toFixed(6)}\nEigenvectors:\n${formatMatrix(pair[1])}`
        ).join('\n\n');
      }
      // Regular matrix or vector
      return formatMatrix(val);
    }
    if (typeof val === 'object' && val !== null) {
      // Handle special outputs
      return JSON.stringify(val, null, 2);
    }
    return String(val);
  };

  if (type === 'input') {
    return (
      <div className="output-line input-line">
        <span className="prompt">{'>>>'}</span> {highlightSyntax(content)}
      </div>
    );
  }

  if (type === 'prompt') {
    return (
      <div className="output-line prompt-line">
        {content}
      </div>
    );
  }

  if (type === 'prompt') {
    return (
      <div className="output-line prompt-line">
        {content}
      </div>
    );
  }

  return (
    <div className={`output-line ${type}`}>
      <pre>{formatContent()}</pre>
    </div>
  );
}

export default Output;
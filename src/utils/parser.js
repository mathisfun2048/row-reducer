// List of functions that require matrix input
const MATRIX_FUNCTIONS = ['rref', 'lu', 'qr', 'inverse', 'det', 'transpose', 'trace', 'rank', 'null',
                          'eigenvalues', 'eigenvectors', 'diagonalize', 'null_space', 'col_space',
                          'row_space', 'lin_ind'];

// List of functions that require vector input
const VECTOR_FUNCTIONS = ['magnitude'];

// List of functions that require two vectors
const TWO_VECTOR_FUNCTIONS = ['dot_product', 'cross', 'projection'];

// List of functions that require two matrices
const TWO_MATRIX_FUNCTIONS = ['matrix_mult', 'change_of_basis'];

// Functions that require matrix and vector
const MATRIX_VECTOR_FUNCTIONS = ['matrix_times_vector', 'solve_system'];

// Parse user commands and execute them
export const parseCommand = (input, workspace) => {
  const trimmed = input.trim();

  // Handle special commands
  if (trimmed === 'clear') {
    return { type: 'clear' };
  }

  if (trimmed === 'vars' || trimmed === 'variables') {
    return { type: 'vars', workspace };
  }

  if (trimmed === 'help') {
    return { type: 'help' };
  }

  if (trimmed === 'documentation' || trimmed === 'docs') {
    return { type: 'documentation' };
  }

  // Show variable: show A
  const showMatch = trimmed.match(/^show\s+([A-Za-z_]\w*)$/);
  if (showMatch) {
    const [, varName] = showMatch;
    return { type: 'show', varName, workspace };
  }

  // Matrix declaration with interactive input: matrix A
  const matrixDeclMatch = trimmed.match(/^matrix\s+([A-Za-z_]\w*)$/);
  if (matrixDeclMatch) {
    const [, varName] = matrixDeclMatch;
    return { type: 'interactive_assign', varName, inputType: 'matrix' };
  }

  // Vector declaration with interactive input: vector v
  const vectorDeclMatch = trimmed.match(/^vector\s+([A-Za-z_]\w*)$/);
  if (vectorDeclMatch) {
    const [, varName] = vectorDeclMatch;
    return { type: 'interactive_assign', varName, inputType: 'vector' };
  }

  // Matrix assignment with literal: matrix A [[1,2],[3,4]] (still supported)
  const matrixMatch = trimmed.match(/^matrix\s+([A-Za-z_]\w*)\s+(\[.+\])$/);
  if (matrixMatch) {
    const [, varName, matrixStr] = matrixMatch;
    try {
      const matrix = JSON.parse(matrixStr);
      return { type: 'assign', varName, value: matrix };
    } catch (e) {
      return { error: 'Invalid matrix format. Use: matrix A [[1,2],[3,4]]' };
    }
  }

  // Vector assignment with literal: vector v [1,2,3] (still supported)
  const vectorMatch = trimmed.match(/^vector\s+([A-Za-z_]\w*)\s+(\[.+\])$/);
  if (vectorMatch) {
    const [, varName, vectorStr] = vectorMatch;
    try {
      const vector = JSON.parse(vectorStr);
      return { type: 'assign', varName, value: vector };
    } catch (e) {
      return { error: 'Invalid vector format. Use: vector v [1,2,3]' };
    }
  }

  // Function call: det(A) or rref(A)
  const funcMatch = trimmed.match(/^([a-z_]\w*)\((.+)\)$/);
  if (funcMatch) {
    const [, funcName, argsStr] = funcMatch;
    const args = argsStr.split(',').map(s => s.trim());
    return { type: 'function', funcName, args };
  }

  // Assignment with function: B = rref(A)
  const assignFuncMatch = trimmed.match(/^([A-Za-z_]\w*)\s*=\s*([a-z_]\w*)\((.+)\)$/);
  if (assignFuncMatch) {
    const [, varName, funcName, argsStr] = assignFuncMatch;
    const args = argsStr.split(',').map(s => s.trim());
    return { type: 'assign_function', varName, funcName, args };
  }

  // Bare function call without arguments (interactive mode)
  const bareFuncMatch = trimmed.match(/^([a-z_]\w*)$/);
  if (bareFuncMatch) {
    const funcName = bareFuncMatch[1];

    // Determine what inputs are needed
    if (MATRIX_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_function', funcName, inputType: 'matrix' };
    }
    if (VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_function', funcName, inputType: 'vector' };
    }
    if (TWO_VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_function', funcName, inputType: 'two_vectors' };
    }
    if (TWO_MATRIX_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_function', funcName, inputType: 'two_matrices' };
    }
    if (MATRIX_VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_function', funcName, inputType: 'matrix_vector' };
    }
  }

  // Assignment with bare function: B = rref (interactive)
  const assignBareFuncMatch = trimmed.match(/^([A-Za-z_]\w*)\s*=\s*([a-z_]\w*)$/);
  if (assignBareFuncMatch) {
    const [, varName, funcName] = assignBareFuncMatch;

    if (MATRIX_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_assign_function', varName, funcName, inputType: 'matrix' };
    }
    if (VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_assign_function', varName, funcName, inputType: 'vector' };
    }
    if (TWO_VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_assign_function', varName, funcName, inputType: 'two_vectors' };
    }
    if (TWO_MATRIX_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_assign_function', varName, funcName, inputType: 'two_matrices' };
    }
    if (MATRIX_VECTOR_FUNCTIONS.includes(funcName)) {
      return { type: 'interactive_assign_function', varName, funcName, inputType: 'matrix_vector' };
    }
  }

  return { error: 'Unknown command. Type "help" for usage.' };
};

export const executeCommand = async (parsed, runPython, workspace) => {
  if (parsed.error) {
    return { error: true, content: parsed.error };
  }

  // Clear command
  if (parsed.type === 'clear') {
    return { content: '' };
  }

  // Show variables
  if (parsed.type === 'vars') {
    if (Object.keys(workspace).length === 0) {
      return { content: 'No variables stored' };
    }
    const vars = Object.entries(workspace)
      .map(([name, value]) => {
        const shape = Array.isArray(value[0])
          ? `${value.length}x${value[0].length}`
          : `${value.length}`;
        return `${name}: ${shape}`;
      })
      .join('\n');
    return { content: vars };
  }

  // Show specific variable
  if (parsed.type === 'show') {
    const { varName, workspace } = parsed;
    if (!workspace[varName]) {
      return { error: true, content: `Variable '${varName}' not found` };
    }
    const value = workspace[varName];

    // Determine if it's a matrix or vector
    const isMatrix = Array.isArray(value[0]);
    const label = isMatrix
      ? `${varName} (${value.length}x${value[0].length} matrix):`
      : `${varName} (vector, length ${value.length}):`;

    return {
      content: {
        label: label,
        value: value
      }
    };
  }

  // Documentation command
  if (parsed.type === 'documentation') {
    try {
      const response = await fetch('/documentation.md');
      const docs = await response.text();
      return { content: docs };
    } catch (error) {
      return { error: true, content: 'Failed to load documentation' };
    }
  }

  // Help command
  if (parsed.type === 'help') {
    return {
      content: `Commands:
matrix A                - Declare matrix A (prompts for input)
vector v                - Declare vector v (prompts for input)
det(A)                  - Call function with variable
B = rref(A)             - Store result in variable B
rref                    - Interactive: prompts for input and displays result
show A                  - Display the contents of variable A
vars                    - Show all stored variables
clear                   - Clear terminal
help                    - Show this message
documentation           - Show detailed function documentation (or 'docs')

Available functions:
rref, lu, qr, det, inverse, transpose, trace, rank, null
eigenvalues, eigenvectors, diagonalize
dot_product, magnitude, cross, projection
matrix_mult, matrix_times_vector, solve_system
null_space, col_space, row_space, lin_ind, change_of_basis

Usage examples:
  matrix A              - Prompts: rows, cols, then each row
  det(A)                - Computes determinant of stored matrix A
  rref                  - Prompts for matrix, displays rref
  B = rref(A)           - Stores rref(A) in B
  show A                - Displays the matrix A
  dot_product           - Prompts for two vectors, displays result

Note: You can still use literal syntax:
  matrix A [[1,2],[3,4]]
  vector v [1,2,3]`
    };
  }

  // Variable assignment
  if (parsed.type === 'assign') {
    const newWorkspace = { ...workspace, [parsed.varName]: parsed.value };
    return { 
      content: `Stored ${parsed.varName}`,
      workspace: newWorkspace 
    };
  }

  // Function call or assignment with function
  const isAssignment = parsed.type === 'assign_function';
  const funcName = parsed.funcName;
  const args = parsed.args;

  // Build Python code
  let pythonCode = '';

  // Add workspace variables to Python
  for (const [name, value] of Object.entries(workspace)) {
    pythonCode += `${name} = ${JSON.stringify(value)}\n`;
  }

  // Process args: if it's a variable name, use it; if it's JSON, parse and add to workspace as temp
  const pythonArgs = args.map((arg, idx) => {
    // Check if it's a variable name in workspace
    if (workspace[arg]) {
      return arg;
    }
    // Check if it's a JSON string (starts with [ or {)
    try {
      JSON.parse(arg);
      // It's a JSON literal, create a temporary variable
      const tempVar = `_temp_${idx}`;
      pythonCode += `${tempVar} = ${arg}\n`;
      return tempVar;
    } catch {
      // Not JSON, treat as variable name
      return arg;
    }
  }).join(', ');

  // Execute function and convert result to JSON for serialization
  pythonCode += `
import json
result = ${funcName}(${pythonArgs})
json.dumps(result)
`;

  console.log('Executing Python code:', pythonCode);
  const result = await runPython(pythonCode);
  console.log('Python result:', result);

  if (result.error) {
    return { error: true, content: result.error };
  }

  // Parse the JSON result
  let parsedResult;
  try {
    parsedResult = JSON.parse(result.result);
  } catch (e) {
    // If it's not JSON, use as-is (for simple types)
    parsedResult = result.result;
  }

  // Add labels to output based on function name
  const labeledResult = addFunctionLabel(funcName, parsedResult);

  // Handle assignment
  if (isAssignment) {
    const newWorkspace = { ...workspace, [parsed.varName]: parsedResult };
    return {
      content: `Stored ${parsed.varName}`,
      workspace: newWorkspace
    };
  }

  // Return result with label
  console.log('Returning content:', labeledResult);
  return { content: labeledResult };
};

// Helper function to add descriptive labels to function outputs
const addFunctionLabel = (funcName, result) => {
  switch (funcName) {
    case 'lu':
      return { label: 'LU Decomposition', parts: ['L (Lower):', 'U (Upper):'], value: result };
    case 'qr':
      return { label: 'QR Decomposition', parts: ['Q (Orthogonal):', 'R (Upper Triangular):'], value: result };
    case 'diagonalize':
      return { label: 'Diagonalization', parts: ['P (Eigenvector Matrix):', 'D (Diagonal Matrix):', 'P⁻¹ (Inverse):'], value: result };
    case 'eigenvectors':
      return { label: 'Eigenvectors', value: result };
    case 'eigenvalues':
      return { label: 'Eigenvalues:', value: result };
    case 'det':
      return { label: 'Determinant:', value: result };
    case 'trace':
      return { label: 'Trace:', value: result };
    case 'rank':
      return { label: 'Rank:', value: result };
    case 'null':
      return { label: 'Nullity:', value: result };
    case 'rref':
      return { label: 'Reduced Row Echelon Form:', value: result };
    case 'inverse':
      return { label: 'Inverse Matrix:', value: result };
    case 'transpose':
      return { label: 'Transpose:', value: result };
    case 'dot_product':
      return { label: 'Dot Product:', value: result };
    case 'magnitude':
      return { label: 'Magnitude:', value: result };
    case 'cross':
      return { label: 'Cross Product:', value: result };
    case 'projection':
      return { label: 'Projection:', value: result };
    case 'matrix_mult':
      return { label: 'Matrix Product:', value: result };
    case 'matrix_times_vector':
      return { label: 'Matrix × Vector:', value: result };
    case 'solve_system':
      return { label: 'Solution Vector:', value: result };
    case 'null_space':
      return { label: 'Null Space Basis:', value: result };
    case 'col_space':
      return { label: 'Column Space Basis:', value: result };
    case 'row_space':
      return { label: 'Row Space Basis:', value: result };
    case 'lin_ind':
      return { label: 'Linearly Independent:', value: result };
    case 'change_of_basis':
      return { label: 'Change of Basis Matrix:', value: result };
    default:
      return { label: null, value: result };
  }
};
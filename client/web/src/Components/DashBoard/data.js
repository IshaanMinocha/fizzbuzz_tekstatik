// data.js
export const vulnerabilities = [
    { id: 1, fuzzResult: 'Buffer Overflow', vulnerability: 'Memory Corruption', severity: 'critical' },
    { id: 2, fuzzResult: 'SQL Injection', vulnerability: 'Input Validation', severity: 'high' },
    { id: 3, fuzzResult: 'Cross-Site Scripting', vulnerability: 'XSS', severity: 'medium' },
    { id: 4, fuzzResult: 'Path Traversal', vulnerability: 'File System Access', severity: 'low' },
    { id: 5, fuzzResult: 'Remote Code Execution', vulnerability: 'Command Injection', severity: 'critical' },
  ];
  
  export const fuzzResultData = [
    {
      id: 1,
      user: 'User 1',
      output: {
        response: 'Response 1',
        lines: 100,
        words: 500,
        chars: 2500,
        timeTaken: '5s',
        payload: 'Payload 1'
      },
      targetUrl: 'http://example.com',
      fuzzType: 'Type 1'
    },
    {
      id: 2,
      user: 'User 2',
      output: {
        response: 'Response 2',
        lines: 120,
        words: 600,
        chars: 3000,
        timeTaken: '6s',
        payload: 'Payload 2'
      },
      targetUrl: 'http://example.org',
      fuzzType: 'Type 2'
    },
 
  ];
  
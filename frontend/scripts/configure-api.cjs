const fs = require('fs');
const apiUrl = (process.env.STACK_UNDERFLOW_API_URL || '/api').replace(/\/$/, '');
if (!/^(https?:\/\/|\/(?!\/))/.test(apiUrl)) throw new Error('API URL must be absolute HTTP(S) or a path starting with /');
fs.writeFileSync('dist/stack-underflow/assets/config.js',
  'window.__STACK_UNDERFLOW_CONFIG__ = ' + JSON.stringify({ apiUrl }) + ';\n');

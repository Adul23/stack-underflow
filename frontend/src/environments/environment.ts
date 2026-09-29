export const environment = {
  production: false,
  apiUrl: ((window as any).__STACK_UNDERFLOW_CONFIG__?.apiUrl || 'http://127.0.0.1:8000/api').replace(/\/$/, '')
};

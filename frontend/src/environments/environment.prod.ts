export const environment = {
  production: true,
  apiUrl: ((window as any).__STACK_UNDERFLOW_CONFIG__?.apiUrl || '/api').replace(/\/$/, '')
};

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// 🔇 SUPRIMIR ERROR BENIGNO "ResizeObserver loop"
// Este error es común en desarrollo con layouts flex/grid complejos y es seguro ignorarlo.
const resizeObserverLoopErr = /ResizeObserver loop completed with undelivered notifications/;
const originalError = console.error;
console.error = (...args) => {
  if (args[0] && resizeObserverLoopErr.test(args[0])) return;
  originalError.call(console, ...args);
};
window.addEventListener('error', (e) => {
  if (resizeObserverLoopErr.test(e.message)) {
    e.stopImmediatePropagation();
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
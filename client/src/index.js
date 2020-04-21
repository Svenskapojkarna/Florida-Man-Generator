import React from 'react';
import ReactDOM from 'react-dom';
import App from './pages/App.jsx';
import * as serviceWorker from './components/serviceWorker';

ReactDOM.render(
  <App />,
  document.getElementById('root')
)
serviceWorker.register();

import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom'
import * as serviceWorker from './components/serviceWorker';
import App from './pages/App.jsx';
import CheckInitialMemes from './pages/CheckInitialMemes'

function AppWrapper(){
  return <App />
}

function CheckInitialMemesWrapper(){
  return <CheckInitialMemes />
}

function render(){
  ReactDOM.render(
  <BrowserRouter>
      <Route exact path="/" component={AppWrapper} />
      <Route path="/articles" component={CheckInitialMemesWrapper} />
  </BrowserRouter>, 
  document.getElementById('root'));
}
render();
serviceWorker.register();

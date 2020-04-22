import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom'
import * as serviceWorker from './components/serviceWorker';
import App from './pages/App.jsx';
import CheckInitialMemes from './pages/CheckInitialMemes'

const api = "http://127.0.0.1:5000/api/"

function AppWrapper(){
  return <App />
}

function CheckInitialMemesWrapper(){
  return <CheckInitialMemes api={api}/>
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

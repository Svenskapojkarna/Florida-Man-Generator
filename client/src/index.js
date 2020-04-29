import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom'
import * as serviceWorker from './components/serviceWorker';
import App from './pages/App.jsx';
import CheckInitialMemes from './pages/CheckInitialMemes'
import CheckUserMemes from './pages/CheckUserMemes'
import CreateNewArticle from './pages/CreateNewArticle'

function AppWrapper(){
  return <App />
}

function CheckInitialMemesWrapper(){
  return <CheckInitialMemes />
}

function CheckUserMemesWrapper(){
  return <CheckUserMemes />
}

function CreateNewArticleWrapper(){
  return <CreateNewArticle />
}

function render(){
  ReactDOM.render(
  <BrowserRouter>
      <Route exact path="/" component={AppWrapper} />
      <Route path="/articles" component={CheckInitialMemesWrapper} />
      <Route path="/myarticles" component={CheckUserMemesWrapper} />
      <Route path="/createarticle" component={CreateNewArticleWrapper} />
  </BrowserRouter>, 
  document.getElementById('root'));
}
render();
serviceWorker.register();

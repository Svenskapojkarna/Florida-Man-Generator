import React from 'react';
import {withRouter} from 'react-router-dom'

class App extends React.Component {
  checkMemesHandle = event => {
    this.props.history.push('/articles')
  }

  checkUserMemesHandle = event => {
    this.props.history.push('/myarticles')
  }

  render(){
    return(
      <div>
        <center>
          <h1>Welcome to Florida Man Generator!</h1>
          <p>What do you want to do today?</p>
          <button onClick={this.checkMemesHandle}>Check a meme</button>
          <button>Create a meme</button>
          <button onClick={this.checkUserMemesHandle}>My memes</button>
        </center>
      </div>
    )
  }
}

export default withRouter(App)

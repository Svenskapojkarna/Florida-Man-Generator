import React from 'react'
import API from '../components/api'
import {withRouter} from 'react-router-dom'

class CreateNewArticle extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            username: null,
            headline: null,
            link: '',
            usersURL: '',
            articlesURL: ''
        }
    }

    componentDidMount(){
        API.get('/api/')
            .then(res => {
                this.setState({
                    usersURL: res.data["@controls"]["floman:users-all"]["href"],
                    articlesURL: res.data["@controls"]["floman:addedarticles-all"]["href"]
                })
            })
    }

    updateUsername = event => {
        event.preventDefault()
        if(event.target.value === ''){
            this.setState({
                username: null
            })
        } else {
            this.setState({
                username: event.target.value
            })
        }
    }

    updateHeadline = event => {
        event.preventDefault()
        if(event.target.value === ''){
            this.setState({
                username: null
            })
        } else {
            this.setState({
                headline: event.target.value
            })
        }
    }

    updateLink = event => {
        event.preventDefault()
        this.setState({
            link: event.target.value
        })
    }

    handleSubmit = async event => {
        event.preventDefault()
        let userPostFailed = false
        let articlePostFailed = false
        const response = await API.get(this.state.usersURL)
        const userschema = response.data["@controls"]["floman:add-user"]["schema"]["properties"]
        const userData = {
            [userschema["username"]["name"]]: this.state.username
        }
        // eslint-disable-next-line
        const response2 = await API.post(this.state.usersURL, userData)
            .catch(error => {
                if(error.response["status"] === 400) {
                    alert('Username and headline cannot be empty')
                } else if(error.response["status"] === 409){
                    alert('Username is already in use.\nIf you want to create a new article for this user, go to My Memes section from main page.')
                 } else {
                    alert('An error occured while posting article\n' + error)
                }
                userPostFailed = true
            })
        if(!userPostFailed){
            const response3 = await API.get(this.state.articlesURL)
            const articleschema = response3.data["@controls"]["floman:add-addedarticle"]["schema"]["properties"]
            const articleData = {
                [articleschema["headline"]["name"]]: this.state.headline,
                [articleschema["link"]["name"]]: this.state.link,
                [articleschema["owner_username"]["name"]]: this.state.username
            }
            // eslint-disable-next-line
            const response4 = await API.post(this.state.articlesURL, articleData)
                .catch(error => {
                    if(error.response["status"] === 400) {
                        alert('Username and headline cannot be empty')
                    } else {
                        alert('An error occured while posting article\n' + error)
                    }
                    articlePostFailed = true
                })
            if(articlePostFailed){
                const response5 = await API.get(this.state.usersURL + this.state.username + '/')
                if (response5.data["items"] === undefined){
                    // eslint-disable-next-line
                    const response6 = await API.delete(this.state.usersURL + this.state.username + '/')
                }
            }
        }
        if(!userPostFailed && !articlePostFailed){
            alert('New article created succesfully!')
        }
    }

    backButton = event => {
        event.preventDefault()
        this.props.history.push('/')
    }

    render() {
        return (
            <div>
                <center>
                    <h1>Create a new Article</h1>
                    <p>Please give your username, headline of the article and link to the article.</p>
                    <form onSubmit={event => event.preventDefault}>
                        <label>Username: </label>
                        <input type='text' onChange={this.updateUsername}/>
                        <label>Headline: </label>
                        <input type='text' onChange={this.updateHeadline}/>
                        <label>Link: </label>
                        <input type='text' onChange={this.updateLink}/>
                        <br />
                        <button onClick={this.handleSubmit}>Submit</button>
                        <button onClick={this.backButton}>Back</button>
                    </form>
                </center>
            </div>
        )
    }
}

export default withRouter(CreateNewArticle)

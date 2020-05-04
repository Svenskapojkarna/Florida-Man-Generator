import React from 'react'
import AddedArticle from '../components/AddedArticle'
import API from '../components/api'
import {withRouter} from 'react-router-dom'

class CheckUserMemes extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            author: '',
            articles: [],
            usersURL: '',
            allArticlesURL: '',
            isAuthor: false,
            create: false,
            newHeadline: null,
            newLink: ''
        }
    }

    componentDidMount() {
        API.get('/api/')
            .then(res => {
                this.setState({
                    usersURL: res.data["@controls"]["floman:users-all"]["href"],
                    allArticlesURL: res.data["@controls"]["floman:addedarticles-all"]["href"]
                })
            })
    }

    setAuthor = event => {
        event.preventDefault()
        this.setState({
            author: event.target.value
        })
    }

    findArticles = async event => {
        event.preventDefault()
        let failed = false
        const response = await API.get(this.state.usersURL + this.state.author + '/')
            .catch(error => {
                alert("No articles found by given user :(")
                failed = true
            })
        if (!failed) {
            const otherResponse = await API.get(response.data["@controls"]["floman:owned-articles"]["href"])
            if (otherResponse.data["items"].length === 0){
                alert("This user hasn't created any articles")
            } else {
                this.setState({
                    isAuthor: true,
                    articles: otherResponse.data["items"],
                })
            }
        }
    }

    findAllArticles = async event => {
        event.preventDefault()
        const response = await API.get(this.state.allArticlesURL)
        this.setState({
            isAuthor: false,
            articles: response.data["items"]
        })
    }

    updateList = async user => {
        const response = await API.get(this.state.usersURL + user + '/')
        this.setState({
            articles: response.data["items"]
        })
    }

    deleteArticle = async (id, user) => {
        // eslint-disable-next-line
        const response = await API.delete(this.state.allArticlesURL + id + '/')
        this.updateList(user)
    }

    backButton = event => {
        event.preventDefault()
        this.props.history.push('/')
    }

    editArticle = async (data, id) => {
        // eslint-disable-next-line
        const response = await API.put((this.state.allArticlesURL + id + '/'), data)
            .catch(error => {
                if (error.response["status"] === 400){
                    alert('Headline cannot be empty')
                } else {
                    alert('Error occured while editing article\n' + error)
                }
            })
        this.updateList(data["owner_username"])
    }

    createArticle = async () => {
        let failed = false
        this.setState({
            create: false
        })
        const data = {
            headline: this.state.newHeadline,
            link: this.state.newLink,
            owner_username: this.state.author
        }
        // eslint-disable-next-line
        const response = await API.post(this.state.allArticlesURL, data)
            .catch(error => {
                if (error.response["status"] === 400){
                    alert('Headline cannot be empty!')
                } else {
                    alert('Error occured when creating new article\n' + error)
                }
                failed = true
            })
        if(!failed){
            alert('New article created succesfully')
        }
    }

    renderCreateArticle = event => {
        event.preventDefault()
        this.setState({
            create: true
        })
    }

    changeHeadline = event => {
        event.preventDefault()
        if (event.target.value === '') {
            this.setState({
                newHeadline: null
            })
        } else {
            this.setState({
                newHeadline: event.target.value
            })
        }
    }

    changeLink = event => {
        event.preventDefault()
        this.setState({
            newLink: event.target.value
        })
    }

    render() {
        const newArticle = (
            <div>
                <form onSubmit={event => event.preventDefault()}>
                    <label><strong>HEADLINE: </strong></label>
                    <input type='text' onChange={this.changeHeadline}/>
                    <label><strong>LINK: </strong></label>
                    <input type='text' onChange={this.changeLink}/>
                    <br />
                    <button onClick={this.createArticle}>Create</button>
                </form>
            </div>
        )
        return(
            <div>
                <center>
                    <h1>My articles</h1>
                    <p>Give the name of the creator</p>
                    <input type='text' placeholder='Author...' onChange={this.setAuthor}/>
                    <br />
                    <button onClick={this.findArticles}>Find articles</button>
                    <button onClick={this.findAllArticles}>See all user created articles</button>
                    <button onClick={this.backButton}>Back</button>
                    {this.state.articles ? this.state.articles.map((article, index) => {
                        return <AddedArticle key={index}
                                        creator={article["owner_username"]}
                                        headline={article["headline"]}
                                        link={article["link"] ? article["link"] : 'No Link'}
                                        id={article["id"]}
                                        delete={this.deleteArticle}
                                        edit={this.editArticle}
                                        author={this.state.isAuthor}/>
                    }) : ''}
                    {this.state.isAuthor ? <button onClick={this.renderCreateArticle}>Create new Article for this user</button> : ''}
                    {this.state.create ? newArticle : ''}
                </center>
            </div>
        )
    }
}

export default withRouter(CheckUserMemes)

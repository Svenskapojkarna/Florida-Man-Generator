import React from 'react'
import AddedArticle from '../components/AddedArticle'
import API from '../components/api'

class CheckUserMemes extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            author: '',
            articles: [],
            usersURL: '',
            allArticlesURL: '',
            isAuthor: false
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
                alert("No articles found by given user :(\n" + error)
                failed = true
            })
        if (!failed) {
            const otherResponse = await API.get(response.data["@controls"]["floman:owned-articles"]["href"])
            if (otherResponse.data["items"].length === 0){
                alert("This user hasn't created any articles")
            } else {
                this.setState({
                    isAuthor: true,
                    articles: otherResponse.data["items"]
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
            .catch(error => {
                this.setState({
                    articles: []
                })
                console.log(error)
            })
        this.setState({
            articles: response.data["items"]
        })
    }

    deleteArticle = async (id, user) => {
        // eslint-disable-next-line
        const response = await API.delete(this.state.allArticlesURL + id + '/')
        this.updateList(user)
    }

    render() {
        return(
            <div>
                <center>
                    <h1>My articles</h1>
                    <p>Give the name of the creator</p>
                    <input type='text' placeholder='Author...' onChange={this.setAuthor}/>
                    <br />
                    <button onClick={this.findArticles}>Find articles</button>
                    <button onClick={this.findAllArticles}>See all user created articles</button>
                    {this.state.articles ? this.state.articles.map((article, index) => {
                        return <AddedArticle key={index}
                                        creator={article["owner_username"]}
                                        headline={article["headline"]}
                                        link={article["link"] ? article["link"] : 'No Link'}
                                        id={article["id"]}
                                        delete={this.deleteArticle}
                                        author={this.state.isAuthor}/>
                    }) : ''}
                </center>
            </div>
        )
    }
}

export default CheckUserMemes

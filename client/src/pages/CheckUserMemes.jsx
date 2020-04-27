import React from 'react'
import Article from '../components/Article'
import API from '../components/api'

class CheckUserMemes extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            author: '',
            articles: [],
            usersURL: ''
        }
    }

    componentDidMount() {
        API.get('/api/')
            .then(res => {
                this.setState({
                    usersURL: res.data["@controls"]["floman:users-all"]["href"]
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
                    articles: otherResponse.data["items"]
                })
            }
        }
    }

    render() {
        return(
            <div>
                <center>
                    <h1>My articles</h1>
                    <p>Give the name of the author</p>
                    <input type='text' placeholder='Author...' onChange={this.setAuthor}/>
                    <button onClick={this.findArticles}>Find articles</button>
                    {this.state.articles.map((article, index) => {
                        return <Article key={index}
                                        date={article["id"]}
                                        headline={article["headline"]}
                                        link={article["link"] ? article["link"] : 'No link'}/>
                    })}
                </center>
            </div>
        )
    }
}

export default CheckUserMemes

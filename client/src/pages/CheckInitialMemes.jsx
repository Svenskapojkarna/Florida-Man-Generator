import React from 'react'
import DatePicker from 'react-datepicker'
import "react-datepicker/dist/react-datepicker.css";
import Article from '../components/Article'
import API from '../components/api'
import {withRouter} from 'react-router-dom'

class CheckInitialMemes extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            articles: [],
            articlesURL: '',
            memeDate: new Date()
        }
    }

    componentDidMount() {
        API.get('/api/')
            .then(res => {
                this.setState({
                    articlesURL: res.data["@controls"]["floman:articles-all"]["href"]
                })
            })
    }

    selectDateHandler = (date) => {
        this.setState({
            memeDate: date
        })
    }

    seeMemeHandler = async event => {
        event.preventDefault()
        let rawmonth = this.state.memeDate.getMonth() + 1
        let month
        if (rawmonth < 10) {
            month = '0' + rawmonth
        } else {
            month = rawmonth
        }
        let rawday = this.state.memeDate.getUTCDate() + 1
        let day
        if (rawday < 10) {
            day = '0' + rawday
        } else {
            day = rawday
        }
        const date = day + '.' + month + '.' + this.state.memeDate.getFullYear()
        let failed = false
        const response = await API.get(this.state.articlesURL + date + '/')
            .catch(error => {
                alert('No articles found with given date :(\n' + error)
                failed = true
            })
        if (!failed){
            this.setState({
                articles: [response.data]
            })
        }
    }

    directToSource = () => {
        window.open(this.state.href)
    }

    showAllArticles = async event => {
        event.preventDefault()
        const response = await API.get(this.state.articlesURL)
        this.setState({
            articles: response.data["items"]
        })
    }

    backButton = event => {
        event.preventDefault()
        this.props.history.push('/')
    }

    render(){
        return(
            <div>
                <center>
                    <h1>Select Florida man article you wish to see</h1>
                    <DatePicker selected={this.state.memeDate}
                                onChange={date => this.selectDateHandler(date)}
                                dateFormat="dd.MM.yyyy"/>
                    <br />
                    <button onClick={this.seeMemeHandler}>See Article</button>
                    <button onClick={this.showAllArticles}>See all Articles</button>
                    <button onClick={this.backButton}>Back</button>
                    {this.state.articles.map((article, index) => {
                        return <Article key={index}
                                        date={article["date"]}
                                        headline={article["headline"]}
                                        link={article["link"]}/>
                    })}
                </center>
            </div>
        )
    }
}

export default withRouter(CheckInitialMemes)
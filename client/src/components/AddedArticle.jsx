import React from 'react'

class AddedArticle extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            edit: false,
            newHeadline: null,
            newLink: ''
        }
    }

    startEdit = event => {
        event.preventDefault()
        this.setState({
            edit: true
        })
    }

    save = event => {
        event.preventDefault()
        this.setState({
            edit: false
        })
        const data = {
            headline: this.state.newHeadline,
            link: this.state.newLink,
            owner_username: this.props.creator
        }
        this.props.edit(data, this.props.id)
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
        const ownerView = (
            <div>
                <strong>CREATOR: </strong>{this.props.creator} <strong>HEADLINE: </strong>{this.props.headline} <strong>LINK: </strong>{this.props.link}
                <button onClick={this.startEdit}>Edit this article</button>
                <button onClick={() => this.props.delete(this.props.id, this.props.creator)}>Delete this article</button>
            </div>
        )
        const normalView = (
            <div>
                <strong>CREATOR: </strong>{this.props.creator} <strong>HEADLINE: </strong>{this.props.headline} <strong>LINK: </strong>{this.props.link}
            </div>
        )
        const editView = (
            <div>
                <strong>CREATOR: </strong>
                    {this.props.creator} 
                <strong>HEADLINE: </strong>
                    <input type='text' onChange={this.changeHeadline}/> 
                <strong>LINK: </strong>
                    <input type='text' onChange={this.changeLink}/>
                <button onClick={this.save}>Save</button>
            </div>
        )
        let renderArticle
        if (this.state.edit) {
            renderArticle = editView
        } else if (this.props.author){
            renderArticle = ownerView
        } else {
            renderArticle = normalView
        }
        return (
            <div>
                {renderArticle}
            </div>
        )
    }
}

export default AddedArticle

import React from 'react'

class Article extends React.Component {
    render() {
        return (
            <div>
                <strong>DATE: </strong>{this.props.date} <strong>HEADLINE: </strong>{this.props.headline} <strong>LINK: </strong>{this.props.link}
            </div>
        )
    }
}

export default Article

import React from 'react'

class AddedArticle extends React.Component {
    render() {
        const editorView = (
            <div>
                <strong>CREATOR: </strong>{this.props.creator} <strong>HEADLINE: </strong>{this.props.headline} <strong>LINK: </strong>{this.props.link}
                <button>Edit this article</button>
                <button onClick={() => this.props.delete(this.props.id, this.props.creator)}>Delete this article</button>
            </div>
        )
        const normalView = (
            <div>
                <strong>CREATOR: </strong>{this.props.creator} <strong>HEADLINE: </strong>{this.props.headline} <strong>LINK: </strong>{this.props.link}
            </div>
        )
        return (
            <div>
                {this.props.author ? editorView : normalView}
            </div>
        )
    }
}

export default AddedArticle

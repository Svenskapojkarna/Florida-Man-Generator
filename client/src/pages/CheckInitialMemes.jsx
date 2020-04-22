import React from 'react'
import DatePicker from 'react-datepicker'
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios'

class CheckInitialMemes extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            MemeDate: new Date(),
            meme: '',
            href: '',
            MemeSelected: false
        }
    }

    selectDateHandler = (date) => {
        this.setState({
            MemeDate: date
        })
    }

    seeMemeHandler = (date) => {
        // Axios stuff
    }

    directToSource = () => {
        window.open(this.state.href)
    }

    render(){
        let meme
        if (this.state.MemeSelected){
            meme = (
                <div>
                    <p>meme: {this.state.meme}</p>
                    <button onClick={this.directToSource}>Source</button>
                </div>
            )
        }

        return(
            <div>
                <center>
                    <h1>Select Florida man article you wish to see</h1>
                    <DatePicker selected={this.state.MemeDate} 
                                onChange={date => this.selectDateHandler(date)}
                                dateFormat="dd.MM.yyyy"/>
                    <br />
                    <button onClick={this.seeMemeHandler('01.01.2020')}>See Meme</button>
                    {meme}
                </center>
            </div>
        )
    }
}

export default CheckInitialMemes
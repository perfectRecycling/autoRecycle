import React, {Component} from 'react';
import LogLink from './LogLink';
import { post } from 'axios';
import './History.css'
import Select from '@material-ui/core/Select'
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Graph from './Graph';


class History extends Component {

    //post 쫙 하면 된다.
    constructor(props) {

		super(props);
        this.onClick= this.onClick.bind(this);
        this.state = { type: 'All', date: '2019-12-19', showResults: false, datas: {} };
        
    }

    onClick = (e) => {

        e.preventDefault()
        this.postfunction()
        .then((response) => {
            this.state.datas = response.data
        })
        console.log(this.state.datas)
        this.setState({showResults: !this.state.showResults});

    }

    handleChange2 = event => {
        this.state.date = event.target.value
        console.log(this.state.date);
    };

    handleChange = event => {
        this.state.type = event.target.value
        console.log(this.state.date);
    };


    postfunction = () =>{
        const url = 'http://15.164.168.205:8080/history';

        const params = {
            garbage_type : this.state.type,
            date : this.state.date
        }

        return post(url, params);
    }

    render(){
        return(
            <div>
                <div>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={this.state.type}
                    className = 'select'
                    onChange={this.handleChange}
                >
                    <MenuItem value={'All'}>All</MenuItem>
                    <MenuItem value={'plastic'}>Plastic</MenuItem>
                    <MenuItem value={'metal'}>Metal</MenuItem>
                    <MenuItem value={'glass'}>Glass</MenuItem>
                    <MenuItem value={'paper'}>Paper</MenuItem>
                </Select>
                
                <TextField
                id="date"
                type="date"
                defaultValue="2019-12-19"
                InputLabelProps={{
                shrink: true,
                }}
                className = 'text'
                onChange ={this.handleChange2}
                />
                <Button type='button' className='formbutton' onClick={this.onClick} color='primary' variant='outlined'>Select</Button>
                </div>
                { this.state.showResults && (<Graph props = {this.state}></Graph>)}
                { this.state.showResults && (<LogLink props = {this.state}></LogLink>)}
            </div>
        )
    };
}

export default History;

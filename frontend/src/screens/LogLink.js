import React, {Component} from 'react';
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import './LogLink.css'
import Log from './Log';
import Button from '@material-ui/core/Button';


class LogLink extends Component {

    constructor(props) {
        super(props);
        this.state = this.props.props
        this.state['showResults'] = [false, false]
        console.log('LogLink')
        console.log(this.state.datas.history)
        this.onClick = this.onClick.bind(this);
    }

    onClick = (idx) => {
        //this.state.showResults = true
        console.log(idx);
        console.log('adnasndnandnsan')
        console.log(this.state.showResults)
        const newState = this.state.showResults;
        newState[idx] = !newState[idx];
        
        this.setState({
            showResults: newState,
        });
    }

    render(){
        const datas = this.state.datas.history;
        
        if(!datas){
            return(<div>Data Loading...</div>)
        }
        return(
            <div>
            <div className='loglink'>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>id</TableCell>
                        <TableCell>Class</TableCell>
                        <TableCell>Date & Time</TableCell>                   
                    </TableRow>
                </TableHead>
                {
                    this.state.datas.history.map((item, idx) =>{return(            
                    <TableBody>
                        <TableRow>
                            <TableCell><Button type='button' color='primary' onClick={() => this.onClick(idx)} variant='outlined'>{item['id']}</Button></TableCell>
                            <TableCell>{item['garbage_type']}</TableCell>  
                            <TableCell>{item['date']}</TableCell>              
                        </TableRow>
                    </TableBody>);})
                }
            </Table>
            </div>
            <div className='logs'>
                {this.state.datas.history.map((item,idx) => {return(
                    <div>{this.state.showResults[idx] && (<Log props={item} ></Log>)}</div>
                );})
                }
            </div>
            </div>
        )
    }
}

export default LogLink;
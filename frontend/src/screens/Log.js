import React, {Component} from 'react';
import './Log.css'
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

class Log extends Component {

    constructor(props) {
        super(props);
        this.state = this.props.props
    }
        
    render(){
        return(
            <div> 
                <div className='log'>
                        <Card>
                            <Typography color="primary">{this.state['id']}-----{this.state['garbage_type']}-----{this.state['date']}</Typography>
                            <img src={this.state['image_path']} className = 'img'></img>
                        </Card>
                </div>
            </div>
        )
    };
}

export default Log;
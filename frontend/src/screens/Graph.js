import React, {Component} from 'react';
import CanvasJSReact from '../canvas/canvasjs.react';
import axios from 'axios';

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph extends Component {

    constructor(props) {
        super(props);
        this.state = this.props.props
        console.log('Graph')
        console.log(this.state)
    }

    addSymbols = (e) => {
		var suffixes = ["", "K", "M", "B"];
		var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
		if(order > suffixes.length - 1)
			order = suffixes.length - 1;
		var suffix = suffixes[order];
		return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
    }

    render(){
        const datas = this.state.datas.chart;
        console.log(datas)

        if(!datas){
            return(<div>Data Loading...</div>)
        }

        const options = {
			animationEnabled: true,
			theme: "light1",
			title:{
				text: "Current recycle state"
			},
			axisX: {
				title: "",
				reversed: true,
			},
			axisY: {
				title: "",
				labelFormatter: this.addSymbols
			},
			data: [{
				type: "bar",
				dataPoints: [
					{ y:  datas[0]['positive_wastedcount'], label: datas[0]['garbage_type'] },
					{ y:  datas[1]['positive_wastedcount'], label: datas[1]['garbage_type'] },
					{ y:  datas[2]['positive_wastedcount'], label: datas[2]['garbage_type'] },
					{ y:  datas[3]['positive_wastedcount'], label: datas[3]['garbage_type'] }
				]
                }
                ]
        }

        return(
            <div className='graph'>
            <CanvasJSChart options = {options}/>
            </div>
        )
    };
}

export default Graph;
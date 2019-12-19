import React, {Component} from 'react';
import CanvasJSReact from '../canvas/canvasjs.react';
import axios from 'axios';

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Today extends Component {

	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this)
		this.state = { datas: {} }
	}

	componentDidMount() {
		console.log('componentDidMount')
		this.handleClick();
		// this.state.datas = {
		// 	chart : [
		// 		{'garbage_type': 'plastic', 'positive_wastedcount': 24},
		// 		{'garbage_type': 'metal', 'positive_wastedcount': 24},
		// 		{'garbage_type': 'glass', 'positive_wastedcount': 24},
		// 		{'garbage_type': 'paper', 'positive_wastedcount': 24}
		// 	]
		// }
	}
	
	handleClick(){
		axios.get('http://15.164.168.205:8080/today/').then((response)=>{
			console.log('response',response);
			this.setState({
				datas: response.data
			});
		})
		.catch((error)=>{
			console.log(error);
		});

	}

	addSymbols(e){
		var suffixes = ["", "K", "M", "B"];
		var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
		if(order > suffixes.length - 1)
			order = suffixes.length - 1;
		var suffix = suffixes[order];
		return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
	}
	
    render() {
		const datas = this.state.datas.chart;

		if (!datas) {
			return (<div>Data Loading..</div>);
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

        
        <CanvasJSChart options = {options}/>
		);
    }
}

export default Today;

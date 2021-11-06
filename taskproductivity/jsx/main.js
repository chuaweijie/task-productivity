import {getCookie} from './helpers.js';
'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const div_main = document.querySelector("#div_main_ui");
   
    if (div_main != null) {
        //Load react component
        ReactDOM.render(<Main/>, div_main);
    }
    else {
        //Load nothing
        console.log("div_main not found!");
    }
});

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: null, 
                        history: null};
    }

    componentDidMount() {
        this.switchTracking = this.switchTracking.bind(this);
        this.switchHistory = this.switchHistory.bind(this);
        this.entryHandler = this.entryHandler.bind(this);
        this.renewalHandler = this.renewalHandler.bind(this);
        this.displayTrackingData = this.displayTrackingData.bind(this);
        this.displayButtons = this.displayButtons.bind(this);
        this.switchTracking();
    }

    switchTracking() {
        fetch(`/tracking`)
        .then(response => response.json())
        .then(data => {
            if (data.error)  {
                console.log(data.error);
            }
            else {
                if (data.status == "no data") {
                    this.displayButtons();
                }
                else if (data.status == "successful") {
                    this.displayTrackingData(data.data);
                }
            }
        });
    }

    displayTrackingData(data) {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Tracking data={data} showButtons={this.displayButtons} displayData={this.displayTrackingData}/>, 
                        history: null});
    }

    displayButtons() {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Buttons entryHandler={this.entryHandler} renewalHandler={this.renewalHandler}/>, 
                        history: null});            
    }

    entryHandler(e) {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <EntryForm submitHandler={this.displayTrackingData} cancelHandler={this.switchTracking}/>, 
                        history: null});            
    }

    renewalHandler(e) {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <RenewalForm cancelHandler={this.switchTracking}/>, 
                        history: null});
    }

    switchHistory(e) {
        this.setState({trackingClass: "nav-link", 
                        historyClass: "nav-link active", 
                        tracking: null, 
                        history: <History/>});
    }

    render() {
        return (
            <div>
                <ul className="nav nav-tabs">
                    <li className="nav-item">
                        <a className={this.state.trackingClass} id="tab_tracking" name="tab_tracking" aria-current="page" href="#" onClick={this.switchTracking}>Tracking</a>
                    </li>
                    <li className="nav-item">
                        <a className={this.state.historyClass} id="tab_history" name="tab_history" aria-current="page" href="#" onClick={this.switchHistory}>History</a>
                    </li>
                </ul>
                {this.state.tracking}
                {this.state.history}
            </div>
        );
    }
}



// Write the UI
class Tracking extends React.Component {
    constructor(props) {
        super(props);
        this.deleteHandler = this.deleteHandler.bind(this);
        this.departHandler = this.departHandler.bind(this);
        this.reportHandler = this.reportHandler.bind(this);
    }

    deleteHandler(e) {
        // TODO have a confirmation dialog before really deleting it. 
        const id = e.target.dataset.id;
        const csrftoken = getCookie('csrftoken');
        fetch('/tracking', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
        .then(response => response.json())
        .then(result =>{
            if(result.error) {
                console.log("Error");
            }
            else {
                if (result.status == "successful") {
                    this.props.showButtons()
                }
            }
        });
        
    }

    departHandler(e) {
        const csrftoken = getCookie('csrftoken');
        fetch('/tracking', {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mode: "departure",
                entry: date
            })
        })
        .then(response => response.json())
        .then(result =>{
            if(result.error) {
                console.log("Error");
            }
            else {
                if (result.status == "successful") {
                    this.props.submitHandler(result.data);
                }
            }
        });
    }

    reportHandler(e) {

    }

    render(){

        const id = this.props.data.id
        const entry = new Date(this.props.data.entry * 1000).toDateString();
        const onlineStart = new Date(this.props.data.online_start * 1000).toDateString();
        const onlineEnd = new Date(this.props.data.online_end * 1000).toDateString();
        const renewal = new Date(this.props.data.renewal * 1000).toDateString();

        return (
            <div>
                <div className="table-responsive">
                    <table className="table">
                        <thead>
                            <tr>
                                <th scope="col">Entry</th>
                                <th scope="col">Online Start</th>
                                <th scope="col">Online End</th>
                                <th scope="col">Renewal</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{entry}</td>
                                <td>{onlineStart}</td>
                                <td>{onlineEnd}</td>
                                <td>{renewal}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-danger mt-3" id="btn_delete" data-id={id} onClick={this.deleteHandler}>Delete</button>
                        </div>
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-secondary mt-3" id="btn_depart" data-id={id} onClick={this.departHandler}>Depart</button>
                        </div>
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-primary mt-3" id="btn_report" data-id={id} onClick={this.reportHandler}>Report</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

// Write the UI
class History extends React.Component {
    constructor(props) {
        super(props);
    }

    render(){
        return (
            <h1>History</h1>
        );
    }
}


class Buttons extends React.Component {
    constructor(props) {
        super(props);
        this.entry = this.entry.bind(this);
        this.renewal = this.renewal.bind(this);
    }

    entry(e) {
        this.props.entryHandler(e);
    }

    renewal(e) {
        this.props.renewalHandler(e);
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm  text-center">
                        <button type="button" id="btn_entry" name="btn_entry" className="btn btn-secondary btn-lg mt-5" onClick={this.entry}>Entry</button>
                    </div>
                    <div className="col-sm  text-center">
                        <button type="button" id="btn_renewal" name="btn_renewal" className="btn btn-primary btn-lg mt-5" onClick={this.renewal}>Renewal Date</button>
                    </div>
                </div>
            </div>
        );
    }
}

class EntryForm extends React.Component {
    constructor(props) {
        super(props);
        this.submit = this.submit.bind(this);
        this.cancel = this.cancel.bind(this);
        this.checkDate = this.checkDate.bind(this);
        this.state = {submitDisabled: true};
    }

    submit(e) {
        const date = Date.parse(document.querySelector("#dateEntry").value) / 1000;
        const csrftoken = getCookie('csrftoken');
        fetch('/tracking', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mode: "entry",
                entry: date
            })
        })
        .then(response => response.json())
        .then(result =>{
            if(result.error) {
                console.log("Error");
            }
            else {
                if (result.status == "successful") {
                    this.props.submitHandler(result.data);
                }
            }
        });
    }

    cancel(e) {
        this.props.cancelHandler(e);
    }

    checkDate(e) {
        console.log(e.target.value);
        console.log(e.target.value.length);
        if (e.target.value.length > 0) {
            this.setState({submitDisabled: false});
        }
        else {
            this.setState({submitDisabled: true});
        }
    }

    render() {
        return (
            <div className="container">
                <form>
                    <div className="form-group mt-4">
                        <label htmlFor="inputEntry">Entry Date</label>
                        <input type="date" className="form-control" id="dateEntry" aria-describedby="dateHelp" placeholder="Enter date" onChange={this.checkDate}/>
                        <small id="dateHelp" className="form-text text-muted">The data that you've entered Thailand</small>
                    </div>
                    <div className="container mt-4">
                        <div className="row">
                            <div className="col-sm  text-center">
                                <button type="submit" className="btn btn-primary mt-3" id="btn_submit" disabled={this.state.submitDisabled} onClick={this.submit}>Submit</button>
                            </div>
                            <div className="col-sm  text-center">
                                <button type="submit" className="btn btn-secondary mt-3" id="btn_cancel" onClick={this.cancel}>Cancel</button>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}

class RenewalForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="container">
               <h1>Reneal Form</h1>
            </div>
        );
    }
}

class DepartureForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="container">
               <h1>Reneal Form</h1>
            </div>
        );
    }
}

class ReportForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="container">
               <h1>Reneal Form</h1>
            </div>
        );
    }
}
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
        this.departureHandler = this.departureHandler.bind(this);
        this.reportedHandler = this.reportedHandler.bind(this);
        this.displayTrackingData = this.displayTrackingData.bind(this);
        this.displayHistoryData = this.displayHistoryData.bind(this);
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

    switchHistory() {
        fetch(`/history`)
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
                    this.displayHistoryData(data.data);
                }
            }
        });
        
    }

    displayTrackingData(data) {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Tracking data={data} showButtons={this.displayButtons} showDepartureForm={this.departureHandler} showReportForm={this.reportedHandler}/>, 
                        history: null});
    }

    displayHistoryData(data) {
        this.setState({trackingClass: "nav-link", 
                        historyClass: "nav-link active", 
                        tracking: null, 
                        history: <History data={data} submitHandler={this.displayHistoryData}/>});
    }

    displayButtons() {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Buttons entryHandler={this.entryHandler} renewalHandler={this.renewalHandler}/>, 
                        history: null});            
    }

    entryHandler(id="null") {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Form mode="entry" submitHandler={this.displayTrackingData} cancelHandler={this.switchTracking} recordId={id}/>, 
                        history: null});            
    }

    renewalHandler(id="null") {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Form mode="renewal" submitHandler={this.displayTrackingData} cancelHandler={this.switchTracking} recordId={id}/>, 
                        history: null});
    }

    departureHandler(id="null") {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Form mode="departure" submitHandler={this.displayButtons}  cancelHandler={this.switchTracking} recordId={id}/>, 
                        history: null});
    }

    reportedHandler(id="null") {
        this.setState({trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Form mode="reported" submitHandler={this.displayTrackingData} cancelHandler={this.switchTracking} recordId={id}/>, 
                        history: null});
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
                    this.props.showButtons();
                }
            }
        });
        
    }

    departHandler(e) {
        const id = e.target.dataset.id;
        this.props.showDepartureForm(id);
    }

    reportHandler(e) {
        const id = e.target.dataset.id;
        this.props.showReportForm(id);
    }

    render(){

        const id = this.props.data.id
        let entry = '-';
        let onlineStart = '-';
        let onlineEnd = '-';
        let renewal = '-';
        if (this.props.data.entry !== null) {
            entry = new Date(this.props.data.entry * 1000).toDateString();
        }
        if (this.props.data.onlineStart !== null) {
            onlineStart = new Date(this.props.data.online_start * 1000).toDateString();
        }

        if (this.props.data.onlineEnd !== null) {
            onlineEnd = new Date(this.props.data.online_end * 1000).toDateString();
        }
        
        if (this.props.data.renewal !== null) {
            renewal = new Date(this.props.data.renewal * 1000).toDateString();
        }

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
                                <td name="row_entry">{entry}</td>
                                <td name="row_online_start">{onlineStart}</td>
                                <td name="row_online_end">{onlineEnd}</td>
                                <td name="row_renewal">{renewal}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-danger mt-3" id="btn_delete" name="btn_delete" data-id={id} onClick={this.deleteHandler}>Delete</button>
                        </div>
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-secondary mt-3" id="btn_depart" name="btn_depart" data-id={id} onClick={this.departHandler}>Depart</button>
                        </div>
                        <div className="col-sm  text-center">
                            <button type="submit" className="btn btn-primary mt-3" id="btn_report" name="btn_report" data-id={id} onClick={this.reportHandler}>Report</button>
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
        this.undoHandler = this.undoHandler.bind(this);
    }

    undoHandler(e) {
        const id = e.target.dataset.id;
        const csrftoken = getCookie('csrftoken');
        fetch('/history', {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mode: "undo",
                id: id,
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

    packData(data) {
        const rows = [];
        let createButton = true;
        data.forEach((row) => {
            let button = "-";
            if (createButton) {
                button = <button type="submit" className="btn btn-primary" id="btn_undo" data-id={row.id} onClick={this.undoHandler}>Undo</button>;
                createButton = false;
            }
            let entry = "-";
            let onlineStart = "-";
            let onlineEnd = "-";
            let renewal = "-";
            let departure = "-";
            let reportedDate = "-";

            if (row.entry  !== null) {
                entry = new Date(row.entry * 1000).toDateString();
            }

            if (row.online_start  !== null) {
                onlineStart = new Date(row.online_start * 1000).toDateString();
            }

            if (row.online_end !== null) {
                onlineEnd = new Date(row.online_end * 1000).toDateString();
            }

            if (row.renewal !== null) {
                renewal = new Date(row.renewal * 1000).toDateString();
            }
            
            if (row.departure !== null ) {
                departure = new Date(row.departure * 1000).toDateString();
            }

            if (row.reported_date !== null) {
                reportedDate = new Date(row.reported_date * 1000).toDateString();
            }
            rows.push(
                <tr key={row.id} name="row_entry">
                    <td>{button}</td>
                    <td>{entry}</td>
                    <td>{onlineStart}</td>
                    <td>{onlineEnd}</td>
                    <td>{renewal}</td>
                    <td>{departure}</td>
                    <td>{reportedDate}</td>
                </tr>
            );
        });
        return rows;
    }

    render(){

        const rows = this.packData(this.props.data);

        return (
            <div className="table-responsive">
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            <th scope="col">Entry</th>
                            <th scope="col">Online Start</th>
                            <th scope="col">Online End</th>
                            <th scope="col">Renewal Date</th>
                            <th scope="col">Departure Date</th>
                            <th scope="col">Reported Date</th>
                        </tr>
                    </thead>
                    <tbody>
                            {rows}
                    </tbody>
                </table>
            </div>
        );
    }
}


class Buttons extends React.Component {
    constructor(props) {
        super(props);
        this.entry = this.entry.bind(this);
        this.renewal = this.renewal.bind(this);
    }

    entry() {
        this.props.entryHandler();
    }

    renewal() {
        this.props.renewalHandler();
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

class Form extends React.Component {
    constructor(props) {
        super(props);
        this.submit = this.submit.bind(this);
        this.cancel = this.cancel.bind(this);
        this.checkDate = this.checkDate.bind(this);
        this.state = {submitDisabled: true};
    }

    submit(e) {
        this.setState({submitDisabled: true});
        const date = Date.parse(document.querySelector("#dateEntry").value) / 1000;
        const csrftoken = getCookie('csrftoken');

        if (this.props.mode == "entry") {
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
                    this.setState({submitDisabled: false});
                }
                else {
                    if (result.status == "successful") {
                        this.props.submitHandler(result.data);
                    }
                }
            });
        }
        else if (this.props.mode == "renewal") {
            fetch('/tracking', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mode: "renewal",
                    renewal: date
                })
            })
            .then(response => response.json())
            .then(result =>{
                if(result.error) {
                    console.log("Error");
                    this.setState({submitDisabled: false});
                }
                else {
                    if (result.status == "successful") {
                        this.props.submitHandler(result.data);
                    }
                }
            });
        }
        else if (this.props.mode == "departure") {
            const id = e.target.dataset.id;
            if (id == "null") {
                console.log("Error: id is null.");
            }
            else {
                fetch('/tracking', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        mode: "departure",
                        id: id,
                        date: date
                    })
                })
                .then(response => response.json())
                .then(result =>{
                    if(result.error) {
                        console.log("Error");
                        this.setState({submitDisabled: false});
                    }
                    else {
                        if (result.status == "successful") {
                            this.props.submitHandler(result.data);
                        }
                    }
                });
            }
        }
        else if (this.props.mode == "reported") {
            const id = e.target.dataset.id;
            if (id == "null") {
                console.log("Error: id is null.");
            }
            else {
                fetch('/tracking', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        mode: "reported",
                        id: id,
                        reported_date: date
                    })
                })
                .then(response => response.json())
                .then(result =>{
                    if(result.error) {
                        console.log("Error");
                        this.setState({submitDisabled: false});
                    }
                    else {
                        if (result.status == "successful") {
                            this.props.submitHandler(result.data);
                        }
                    }
                });
            }
        }
    }

    cancel() {
        this.props.cancelHandler();
    }

    checkDate(e) {
        if (e.target.value.length > 0) {
            this.setState({submitDisabled: false});
        }
        else {
            this.setState({submitDisabled: true});
        }
    }

    render() {
        
        let label = "";
        let labelHelp = "";
        const id = this.props.recordId;
        
        if (this.props.mode == "renewal") {
            label = "Renewal Date";
            labelHelp = "The date that you will need to give your 90 days notification";
        }
        else if (this.props.mode == "entry") {
            label = "Entry Date";
            labelHelp = "The date that you've entered Thailand";
        }
        else if (this.props.mode == "departure") {
            label = "Departure Date";
            labelHelp = "The date that you left Thailand";
        }
        else if (this.props.mode == "reported") {
            label = "Entry Date";
            labelHelp = "The date that you've given your 90 days notification";
        }


        return (
            <div className="container">
                <form>
                    <div className="form-group mt-4">
                        <label htmlFor="inputEntry">{label}</label>
                        <input type="date" className="form-control" id="dateEntry" aria-describedby="dateHelp" placeholder="Enter date" onChange={this.checkDate}/>
                        <small id="dateHelp" className="form-text text-muted">{labelHelp}</small>
                    </div>
                    <div className="container mt-4">
                        <div className="row">
                            <div className="col-sm  text-center">
                                <button type="submit" className="btn btn-primary mt-3" id="btn_submit" data-id={id} disabled={this.state.submitDisabled} onClick={this.submit}>Submit</button>
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
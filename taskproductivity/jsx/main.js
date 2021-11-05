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
        this.switchTracking = this.switchTracking.bind(this);
        this.switchHistory = this.switchHistory.bind(this);
        this.state = {trackingClass: "nav-link active", 
                        historyClass: "nav-link", 
                        tracking: <Tracking/>, 
                        history: null};
        this.switchTracking()
    }

    switchTracking(e) {
        fetch(`/tracking`)
        .then(response => response.json())
        .then(data => {
            if (data.error)  {
                console.log(data.error);
            }
            else {
                if (data.status == "no data") {
                    this.setState({trackingClass: "nav-link active", 
                                    historyClass: "nav-link", 
                                    tracking: <Buttons/>, 
                                    history: null});            
                }
                else if (data.status == "successful") {
                    this.setState({trackingClass: "nav-link active", 
                                    historyClass: "nav-link", 
                                    tracking: <Tracking/>, 
                                    history: null});
                }
            }
        });
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
    }

    render(){
        return (
            <table className="table">
                <thead>
                    <tr>
                        <th scope="col">Entry</th>
                        <th scope="col">Online Start</th>
                        <th scope="col">Online End</th>
                        <th scope="col">Renewal</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
            </table>
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
    }

    render(){
        return (
            <div className="container">
                <div className="row">
                    <div className="col-sm  text-center">
                        <button type="button" className="btn btn-secondary btn-lg mt-5">Entry</button>
                    </div>
                    <div className="col-sm  text-center">
                        <button type="button" className="btn btn-primary btn-lg mt-5">Renewal Date</button>
                    </div>
                </div>
            </div>
        );
    }
}
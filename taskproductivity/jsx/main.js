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
        this.state = {trackingClass: "nav-link active", historyClass: "nav-link", tracking: <Tracking/>, history: null};
    }

    switchTracking(e) {
        this.setState({trackingClass: "nav-link active", historyClass: "nav-link", tracking: <Tracking/>, history: null});
    }

    switchHistory(e) {
        this.setState({trackingClass: "nav-link", historyClass: "nav-link active", tracking: null, history: <History/>});
    }

    render() {
        return (
            <div>
                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <a class={this.state.trackingClass} id="tab_tracking" name="tab_tracking" aria-current="page" href="#" onClick={this.switchTracking}>Tracking</a>
                    </li>
                    <li class="nav-item">
                        <a class={this.state.historyClass} id="tab_history" name="tab_history" aria-current="page" href="#" onClick={this.switchHistory}>History</a>
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
            <h1>Tracking</h1>
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
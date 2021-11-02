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
        this.state = {trackingClass: "nav-link active", historyClass: "nav-link"};
    }

    switchTracking(e) {
        this.setState({trackingClass: "nav-link active", historyClass: "nav-link"});
    }

    switchHistory(e) {
        this.setState({trackingClass: "nav-link", historyClass: "nav-link active"});
    }

    render() {
        return (
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class={this.state.trackingClass} id="tab_tracking" name="tab_tracking" aria-current="page" href="#" onClick={this.switchTracking}>Tracking</a>
                </li>
                <li class="nav-item">
                    <a class={this.state.historyClass} id="tab_history" name="tab_history" aria-current="page" href="#" onClick={this.switchHistory}>History</a>
                </li>
            </ul>
        );
    }
}



// Write the UI
/*class Tracking extends React.Component {
    constructor(props) {
        super(props);
        this.newPost = this.newPost.bind(this);
        this.checkTxtArea = this.checkTxtArea.bind(this);
        this.state = {btn_disabled: true, value: ""};
    }

    newPost(e) {
        const post_text = document.querySelector("#txtarea_post");
        const csrftoken = getCookie('csrftoken');
        fetch('/save_post', {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                post: post_text.value
            })
        })
        .then(response => response.json())
        .then(result =>{
            if(result.error) {
                console.log("Error");
            }
            else {
                this.setState({btn_disabled: true, value: ""});
                getAllPosts('#posts');
            }
        });
    }

    checkTxtArea(e) {
        if (e.target.value.length > 0) {
            this.setState({btn_disabled: false, value: e.target.value});
        }
        else {
            this.setState({btn_disabled: true, value: ""});
        }
    }

    render(){
        return (
            <div className="form-floating">
                <textarea className="form-control" id="txtarea_post" name="txtarea_post" style={{height: 100+'px'}} onChange={this.checkTxtArea} value={this.state.value}></textarea>
                <label htmlFor="txtarea_post">Post</label>
                <button type="button" disabled={this.state.btn_disabled} className="btn btn-primary mt-1" id="btn_post" name="btn_post" onClick={this.newPost}>Post</button>
            </div>
        );
    }
}

// Write the UI
class History extends React.Component {
    constructor(props) {
        super(props);
        this.newPost = this.newPost.bind(this);
        this.checkTxtArea = this.checkTxtArea.bind(this);
        this.state = {btn_disabled: true, value: ""};
    }

    newPost(e) {
        const post_text = document.querySelector("#txtarea_post");
        const csrftoken = getCookie('csrftoken');
        fetch('/save_post', {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                post: post_text.value
            })
        })
        .then(response => response.json())
        .then(result =>{
            if(result.error) {
                console.log("Error");
            }
            else {
                this.setState({btn_disabled: true, value: ""});
                getAllPosts('#posts');
            }
        });
    }

    checkTxtArea(e) {
        if (e.target.value.length > 0) {
            this.setState({btn_disabled: false, value: e.target.value});
        }
        else {
            this.setState({btn_disabled: true, value: ""});
        }
    }

    render(){
        return (
            <div className="form-floating">
                <textarea className="form-control" id="txtarea_post" name="txtarea_post" style={{height: 100+'px'}} onChange={this.checkTxtArea} value={this.state.value}></textarea>
                <label htmlFor="txtarea_post">Post</label>
                <button type="button" disabled={this.state.btn_disabled} className="btn btn-primary mt-1" id="btn_post" name="btn_post" onClick={this.newPost}>Post</button>
            </div>
        );
    }
}*/
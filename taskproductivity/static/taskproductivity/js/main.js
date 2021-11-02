'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

document.addEventListener('DOMContentLoaded', function () {
    var div_main = document.querySelector("#div_main_ui");

    if (div_main != null) {
        //Load react component
        ReactDOM.render(React.createElement(Main, null), div_main);
    } else {
        //Load nothing
        console.log("div_main not found!");
    }
});

var Main = function (_React$Component) {
    _inherits(Main, _React$Component);

    function Main(props) {
        _classCallCheck(this, Main);

        var _this = _possibleConstructorReturn(this, (Main.__proto__ || Object.getPrototypeOf(Main)).call(this, props));

        _this.switchTracking = _this.switchTracking.bind(_this);
        _this.switchHistory = _this.switchHistory.bind(_this);
        _this.state = { trackingClass: "nav-link active", historyClass: "nav-link" };
        return _this;
    }

    _createClass(Main, [{
        key: 'switchTracking',
        value: function switchTracking(e) {
            this.setState({ trackingClass: "nav-link active", historyClass: "nav-link" });
        }
    }, {
        key: 'switchHistory',
        value: function switchHistory(e) {
            this.setState({ trackingClass: "nav-link", historyClass: "nav-link active" });
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'ul',
                { 'class': 'nav nav-tabs' },
                React.createElement(
                    'li',
                    { 'class': 'nav-item' },
                    React.createElement(
                        'a',
                        { 'class': this.state.trackingClass, id: 'tab_tracking', name: 'tab_tracking', 'aria-current': 'page', href: '#', onClick: this.switchTracking },
                        'Tracking'
                    )
                ),
                React.createElement(
                    'li',
                    { 'class': 'nav-item' },
                    React.createElement(
                        'a',
                        { 'class': this.state.historyClass, id: 'tab_history', name: 'tab_history', 'aria-current': 'page', href: '#', onClick: this.switchHistory },
                        'History'
                    )
                )
            );
        }
    }]);

    return Main;
}(React.Component);

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
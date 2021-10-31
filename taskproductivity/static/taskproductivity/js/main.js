var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

document.addEventListener('DOMContentLoaded', function () {
    var div_main = document.querySelector("#div_main_ui");

    if (div_main != null) {
        //Load react component
        console.log("div_main found!");
    } else {
        //Load nothing
        console.log("div_main not found!");
    }
});

// Write the UI

var Tracking = function (_React$Component) {
    _inherits(Tracking, _React$Component);

    function Tracking(props) {
        _classCallCheck(this, Tracking);

        var _this = _possibleConstructorReturn(this, (Tracking.__proto__ || Object.getPrototypeOf(Tracking)).call(this, props));

        _this.newPost = _this.newPost.bind(_this);
        _this.checkTxtArea = _this.checkTxtArea.bind(_this);
        _this.state = { btn_disabled: true, value: "" };
        return _this;
    }

    _createClass(Tracking, [{
        key: "newPost",
        value: function newPost(e) {
            var _this2 = this;

            var post_text = document.querySelector("#txtarea_post");
            var csrftoken = getCookie('csrftoken');
            fetch('/save_post', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    post: post_text.value
                })
            }).then(function (response) {
                return response.json();
            }).then(function (result) {
                if (result.error) {
                    console.log("Error");
                } else {
                    _this2.setState({ btn_disabled: true, value: "" });
                    getAllPosts('#posts');
                }
            });
        }
    }, {
        key: "checkTxtArea",
        value: function checkTxtArea(e) {
            if (e.target.value.length > 0) {
                this.setState({ btn_disabled: false, value: e.target.value });
            } else {
                this.setState({ btn_disabled: true, value: "" });
            }
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "form-floating" },
                React.createElement("textarea", { className: "form-control", id: "txtarea_post", name: "txtarea_post", style: { height: 100 + 'px' }, onChange: this.checkTxtArea, value: this.state.value }),
                React.createElement(
                    "label",
                    { htmlFor: "txtarea_post" },
                    "Post"
                ),
                React.createElement(
                    "button",
                    { type: "button", disabled: this.state.btn_disabled, className: "btn btn-primary mt-1", id: "btn_post", name: "btn_post", onClick: this.newPost },
                    "Post"
                )
            );
        }
    }]);

    return Tracking;
}(React.Component);

// Write the UI


var History = function (_React$Component2) {
    _inherits(History, _React$Component2);

    function History(props) {
        _classCallCheck(this, History);

        var _this3 = _possibleConstructorReturn(this, (History.__proto__ || Object.getPrototypeOf(History)).call(this, props));

        _this3.newPost = _this3.newPost.bind(_this3);
        _this3.checkTxtArea = _this3.checkTxtArea.bind(_this3);
        _this3.state = { btn_disabled: true, value: "" };
        return _this3;
    }

    _createClass(History, [{
        key: "newPost",
        value: function newPost(e) {
            var _this4 = this;

            var post_text = document.querySelector("#txtarea_post");
            var csrftoken = getCookie('csrftoken');
            fetch('/save_post', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    post: post_text.value
                })
            }).then(function (response) {
                return response.json();
            }).then(function (result) {
                if (result.error) {
                    console.log("Error");
                } else {
                    _this4.setState({ btn_disabled: true, value: "" });
                    getAllPosts('#posts');
                }
            });
        }
    }, {
        key: "checkTxtArea",
        value: function checkTxtArea(e) {
            if (e.target.value.length > 0) {
                this.setState({ btn_disabled: false, value: e.target.value });
            } else {
                this.setState({ btn_disabled: true, value: "" });
            }
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "form-floating" },
                React.createElement("textarea", { className: "form-control", id: "txtarea_post", name: "txtarea_post", style: { height: 100 + 'px' }, onChange: this.checkTxtArea, value: this.state.value }),
                React.createElement(
                    "label",
                    { htmlFor: "txtarea_post" },
                    "Post"
                ),
                React.createElement(
                    "button",
                    { type: "button", disabled: this.state.btn_disabled, className: "btn btn-primary mt-1", id: "btn_post", name: "btn_post", onClick: this.newPost },
                    "Post"
                )
            );
        }
    }]);

    return History;
}(React.Component);
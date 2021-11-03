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
        _this.state = { trackingClass: "nav-link active", historyClass: "nav-link", tracking: React.createElement(Tracking, null), history: null };
        return _this;
    }

    _createClass(Main, [{
        key: 'switchTracking',
        value: function switchTracking(e) {
            fetch('/tracking').then(function (response) {
                return response.json();
            }).then(function (data) {
                if (data.error) {
                    console.log(data.error);
                } else {
                    console.log(data);
                }
            });
            this.setState({ trackingClass: "nav-link active", historyClass: "nav-link", tracking: React.createElement(Tracking, null), history: null });
        }
    }, {
        key: 'switchHistory',
        value: function switchHistory(e) {
            this.setState({ trackingClass: "nav-link", historyClass: "nav-link active", tracking: null, history: React.createElement(History, null) });
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                null,
                React.createElement(
                    'ul',
                    { className: 'nav nav-tabs' },
                    React.createElement(
                        'li',
                        { className: 'nav-item' },
                        React.createElement(
                            'a',
                            { className: this.state.trackingClass, id: 'tab_tracking', name: 'tab_tracking', 'aria-current': 'page', href: '#', onClick: this.switchTracking },
                            'Tracking'
                        )
                    ),
                    React.createElement(
                        'li',
                        { className: 'nav-item' },
                        React.createElement(
                            'a',
                            { className: this.state.historyClass, id: 'tab_history', name: 'tab_history', 'aria-current': 'page', href: '#', onClick: this.switchHistory },
                            'History'
                        )
                    )
                ),
                this.state.tracking,
                this.state.history
            );
        }
    }]);

    return Main;
}(React.Component);

// Write the UI


var Tracking = function (_React$Component2) {
    _inherits(Tracking, _React$Component2);

    function Tracking(props) {
        _classCallCheck(this, Tracking);

        return _possibleConstructorReturn(this, (Tracking.__proto__ || Object.getPrototypeOf(Tracking)).call(this, props));
    }

    _createClass(Tracking, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'table',
                { className: 'table' },
                React.createElement(
                    'thead',
                    null,
                    React.createElement(
                        'tr',
                        null,
                        React.createElement(
                            'th',
                            { scope: 'col' },
                            'Entry'
                        ),
                        React.createElement(
                            'th',
                            { scope: 'col' },
                            'Online Start'
                        ),
                        React.createElement(
                            'th',
                            { scope: 'col' },
                            'Online End'
                        ),
                        React.createElement(
                            'th',
                            { scope: 'col' },
                            'Renewal'
                        ),
                        React.createElement('th', { scope: 'col' })
                    )
                )
            );
        }
    }]);

    return Tracking;
}(React.Component);

// Write the UI


var History = function (_React$Component3) {
    _inherits(History, _React$Component3);

    function History(props) {
        _classCallCheck(this, History);

        return _possibleConstructorReturn(this, (History.__proto__ || Object.getPrototypeOf(History)).call(this, props));
    }

    _createClass(History, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'h1',
                null,
                'History'
            );
        }
    }]);

    return History;
}(React.Component);
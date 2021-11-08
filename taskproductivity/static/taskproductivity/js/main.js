var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import { getCookie } from './helpers.js';
'use strict';

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

        _this.state = { trackingClass: "nav-link active",
            historyClass: "nav-link",
            tracking: null,
            history: null };
        return _this;
    }

    _createClass(Main, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
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
    }, {
        key: 'switchTracking',
        value: function switchTracking() {
            var _this2 = this;

            fetch('/tracking').then(function (response) {
                return response.json();
            }).then(function (data) {
                if (data.error) {
                    console.log(data.error);
                } else {
                    if (data.status == "no data") {
                        _this2.displayButtons();
                    } else if (data.status == "successful") {
                        _this2.displayTrackingData(data.data);
                    }
                }
            });
        }
    }, {
        key: 'switchHistory',
        value: function switchHistory() {
            var _this3 = this;

            fetch('/history').then(function (response) {
                return response.json();
            }).then(function (data) {
                if (data.error) {
                    console.log(data.error);
                } else {
                    if (data.status == "no data") {
                        _this3.displayButtons();
                    } else if (data.status == "successful") {
                        _this3.displayHistoryData(data.data);
                    }
                }
            });
        }
    }, {
        key: 'displayTrackingData',
        value: function displayTrackingData(data) {
            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Tracking, { data: data, showButtons: this.displayButtons, showDepartureForm: this.departureHandler, showReportForm: this.reportedHandler }),
                history: null });
        }
    }, {
        key: 'displayHistoryData',
        value: function displayHistoryData(data) {
            this.setState({ trackingClass: "nav-link",
                historyClass: "nav-link active",
                tracking: null,
                history: React.createElement(History, { data: data, submitHandler: this.displayHistoryData }) });
        }
    }, {
        key: 'displayButtons',
        value: function displayButtons() {
            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Buttons, { entryHandler: this.entryHandler, renewalHandler: this.renewalHandler }),
                history: null });
        }
    }, {
        key: 'entryHandler',
        value: function entryHandler() {
            var id = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "null";

            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Form, { mode: 'entry', submitHandler: this.displayTrackingData, cancelHandler: this.switchTracking, recordId: id }),
                history: null });
        }
    }, {
        key: 'renewalHandler',
        value: function renewalHandler() {
            var id = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "null";

            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Form, { mode: 'renewal', submitHandler: this.displayTrackingData, cancelHandler: this.switchTracking, recordId: id }),
                history: null });
        }
    }, {
        key: 'departureHandler',
        value: function departureHandler() {
            var id = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "null";

            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Form, { mode: 'departure', submitHandler: this.displayButtons, cancelHandler: this.switchTracking, recordId: id }),
                history: null });
        }
    }, {
        key: 'reportedHandler',
        value: function reportedHandler() {
            var id = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "null";

            this.setState({ trackingClass: "nav-link active",
                historyClass: "nav-link",
                tracking: React.createElement(Form, { mode: 'reported', submitHandler: this.displayTrackingData, cancelHandler: this.switchTracking, recordId: id }),
                history: null });
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

        var _this4 = _possibleConstructorReturn(this, (Tracking.__proto__ || Object.getPrototypeOf(Tracking)).call(this, props));

        _this4.deleteHandler = _this4.deleteHandler.bind(_this4);
        _this4.departHandler = _this4.departHandler.bind(_this4);
        _this4.reportHandler = _this4.reportHandler.bind(_this4);
        return _this4;
    }

    _createClass(Tracking, [{
        key: 'deleteHandler',
        value: function deleteHandler(e) {
            var _this5 = this;

            // TODO have a confirmation dialog before really deleting it. 
            var id = e.target.dataset.id;
            var csrftoken = getCookie('csrftoken');
            fetch('/tracking', {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: id
                })
            }).then(function (response) {
                return response.json();
            }).then(function (result) {
                if (result.error) {
                    console.log("Error");
                } else {
                    if (result.status == "successful") {
                        _this5.props.showButtons();
                    }
                }
            });
        }
    }, {
        key: 'departHandler',
        value: function departHandler(e) {
            var id = e.target.dataset.id;
            this.props.showDepartureForm(id);
        }
    }, {
        key: 'reportHandler',
        value: function reportHandler(e) {
            var id = e.target.dataset.id;
            this.props.showReportForm(id);
        }
    }, {
        key: 'render',
        value: function render() {

            var id = this.props.data.id;
            var entry = '-';
            var onlineStart = '-';
            var onlineEnd = '-';
            var renewal = '-';
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

            return React.createElement(
                'div',
                null,
                React.createElement(
                    'div',
                    { className: 'table-responsive' },
                    React.createElement(
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
                                )
                            )
                        ),
                        React.createElement(
                            'tbody',
                            null,
                            React.createElement(
                                'tr',
                                null,
                                React.createElement(
                                    'td',
                                    { name: 'row_entry' },
                                    entry
                                ),
                                React.createElement(
                                    'td',
                                    { name: 'row_online_start' },
                                    onlineStart
                                ),
                                React.createElement(
                                    'td',
                                    { name: 'row_online_end' },
                                    onlineEnd
                                ),
                                React.createElement(
                                    'td',
                                    { name: 'row_renewal' },
                                    renewal
                                )
                            )
                        )
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'container' },
                    React.createElement(
                        'div',
                        { className: 'row' },
                        React.createElement(
                            'div',
                            { className: 'col-sm  text-center' },
                            React.createElement(
                                'button',
                                { type: 'submit', className: 'btn btn-danger mt-3', id: 'btn_delete', name: 'btn_delete', 'data-id': id, onClick: this.deleteHandler },
                                'Delete'
                            )
                        ),
                        React.createElement(
                            'div',
                            { className: 'col-sm  text-center' },
                            React.createElement(
                                'button',
                                { type: 'submit', className: 'btn btn-secondary mt-3', id: 'btn_depart', name: 'btn_depart', 'data-id': id, onClick: this.departHandler },
                                'Depart'
                            )
                        ),
                        React.createElement(
                            'div',
                            { className: 'col-sm  text-center' },
                            React.createElement(
                                'button',
                                { type: 'submit', className: 'btn btn-primary mt-3', id: 'btn_report', name: 'btn_report', 'data-id': id, onClick: this.reportHandler },
                                'Report'
                            )
                        )
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

        var _this6 = _possibleConstructorReturn(this, (History.__proto__ || Object.getPrototypeOf(History)).call(this, props));

        _this6.undoHandler = _this6.undoHandler.bind(_this6);
        return _this6;
    }

    _createClass(History, [{
        key: 'undoHandler',
        value: function undoHandler(e) {
            var _this7 = this;

            var id = e.target.dataset.id;
            var csrftoken = getCookie('csrftoken');
            fetch('/history', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mode: "undo",
                    id: id
                })
            }).then(function (response) {
                return response.json();
            }).then(function (result) {
                if (result.error) {
                    console.log("Error");
                } else {
                    if (result.status == "successful") {
                        _this7.props.submitHandler(result.data);
                    }
                }
            });
        }
    }, {
        key: 'packData',
        value: function packData(data) {
            var _this8 = this;

            var rows = [];
            var createButton = true;
            data.forEach(function (row) {
                var button = "-";
                if (createButton) {
                    button = React.createElement(
                        'button',
                        { type: 'submit', className: 'btn btn-primary', id: 'btn_undo', 'data-id': row.id, onClick: _this8.undoHandler },
                        'Undo'
                    );
                    createButton = false;
                }
                var entry = "-";
                var onlineStart = "-";
                var onlineEnd = "-";
                var renewal = "-";
                var departure = "-";
                var reportedDate = "-";

                if (row.entry !== null) {
                    entry = new Date(row.entry * 1000).toDateString();
                }

                if (row.online_start !== null) {
                    onlineStart = new Date(row.online_start * 1000).toDateString();
                }

                if (row.online_end !== null) {
                    onlineEnd = new Date(row.online_end * 1000).toDateString();
                }

                if (row.renewal !== null) {
                    renewal = new Date(row.renewal * 1000).toDateString();
                }

                if (row.departure !== null) {
                    departure = new Date(row.departure * 1000).toDateString();
                }

                if (row.reported_date !== null) {
                    reportedDate = new Date(row.reported_date * 1000).toDateString();
                }
                rows.push(React.createElement(
                    'tr',
                    { key: row.id, name: 'row_entry' },
                    React.createElement(
                        'td',
                        null,
                        button
                    ),
                    React.createElement(
                        'td',
                        null,
                        entry
                    ),
                    React.createElement(
                        'td',
                        null,
                        onlineStart
                    ),
                    React.createElement(
                        'td',
                        null,
                        onlineEnd
                    ),
                    React.createElement(
                        'td',
                        null,
                        renewal
                    ),
                    React.createElement(
                        'td',
                        null,
                        departure
                    ),
                    React.createElement(
                        'td',
                        null,
                        reportedDate
                    )
                ));
            });
            return rows;
        }
    }, {
        key: 'render',
        value: function render() {

            var rows = this.packData(this.props.data);

            return React.createElement(
                'div',
                { className: 'table-responsive' },
                React.createElement(
                    'table',
                    { className: 'table' },
                    React.createElement(
                        'thead',
                        null,
                        React.createElement(
                            'tr',
                            null,
                            React.createElement('th', { scope: 'col' }),
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
                                'Renewal Date'
                            ),
                            React.createElement(
                                'th',
                                { scope: 'col' },
                                'Departure Date'
                            ),
                            React.createElement(
                                'th',
                                { scope: 'col' },
                                'Reported Date'
                            )
                        )
                    ),
                    React.createElement(
                        'tbody',
                        null,
                        rows
                    )
                )
            );
        }
    }]);

    return History;
}(React.Component);

var Buttons = function (_React$Component4) {
    _inherits(Buttons, _React$Component4);

    function Buttons(props) {
        _classCallCheck(this, Buttons);

        var _this9 = _possibleConstructorReturn(this, (Buttons.__proto__ || Object.getPrototypeOf(Buttons)).call(this, props));

        _this9.entry = _this9.entry.bind(_this9);
        _this9.renewal = _this9.renewal.bind(_this9);
        return _this9;
    }

    _createClass(Buttons, [{
        key: 'entry',
        value: function entry() {
            this.props.entryHandler();
        }
    }, {
        key: 'renewal',
        value: function renewal() {
            this.props.renewalHandler();
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                { className: 'container' },
                React.createElement(
                    'div',
                    { className: 'row' },
                    React.createElement(
                        'div',
                        { className: 'col-sm  text-center' },
                        React.createElement(
                            'button',
                            { type: 'button', id: 'btn_entry', name: 'btn_entry', className: 'btn btn-secondary btn-lg mt-5', onClick: this.entry },
                            'Entry'
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'col-sm  text-center' },
                        React.createElement(
                            'button',
                            { type: 'button', id: 'btn_renewal', name: 'btn_renewal', className: 'btn btn-primary btn-lg mt-5', onClick: this.renewal },
                            'Renewal Date'
                        )
                    )
                )
            );
        }
    }]);

    return Buttons;
}(React.Component);

var Form = function (_React$Component5) {
    _inherits(Form, _React$Component5);

    function Form(props) {
        _classCallCheck(this, Form);

        var _this10 = _possibleConstructorReturn(this, (Form.__proto__ || Object.getPrototypeOf(Form)).call(this, props));

        _this10.submit = _this10.submit.bind(_this10);
        _this10.cancel = _this10.cancel.bind(_this10);
        _this10.checkDate = _this10.checkDate.bind(_this10);
        _this10.state = { submitDisabled: true };
        return _this10;
    }

    _createClass(Form, [{
        key: 'submit',
        value: function submit(e) {
            var _this11 = this;

            this.setState({ submitDisabled: true });
            var date = Date.parse(document.querySelector("#dateEntry").value) / 1000;
            var csrftoken = getCookie('csrftoken');

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
                }).then(function (response) {
                    return response.json();
                }).then(function (result) {
                    if (result.error) {
                        console.log("Error");
                        _this11.setState({ submitDisabled: false });
                    } else {
                        if (result.status == "successful") {
                            _this11.props.submitHandler(result.data);
                        }
                    }
                });
            } else if (this.props.mode == "renewal") {
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
                }).then(function (response) {
                    return response.json();
                }).then(function (result) {
                    if (result.error) {
                        console.log("Error");
                        _this11.setState({ submitDisabled: false });
                    } else {
                        if (result.status == "successful") {
                            _this11.props.submitHandler(result.data);
                        }
                    }
                });
            } else if (this.props.mode == "departure") {
                var id = e.target.dataset.id;
                if (id == "null") {
                    console.log("Error: id is null.");
                } else {
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
                    }).then(function (response) {
                        return response.json();
                    }).then(function (result) {
                        if (result.error) {
                            console.log("Error");
                            _this11.setState({ submitDisabled: false });
                        } else {
                            if (result.status == "successful") {
                                _this11.props.submitHandler(result.data);
                            }
                        }
                    });
                }
            } else if (this.props.mode == "reported") {
                var _id = e.target.dataset.id;
                if (_id == "null") {
                    console.log("Error: id is null.");
                } else {
                    fetch('/tracking', {
                        method: 'PUT',
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            mode: "reported",
                            id: _id,
                            reported_date: date
                        })
                    }).then(function (response) {
                        return response.json();
                    }).then(function (result) {
                        if (result.error) {
                            console.log("Error");
                            _this11.setState({ submitDisabled: false });
                        } else {
                            if (result.status == "successful") {
                                _this11.props.submitHandler(result.data);
                            }
                        }
                    });
                }
            }
        }
    }, {
        key: 'cancel',
        value: function cancel() {
            this.props.cancelHandler();
        }
    }, {
        key: 'checkDate',
        value: function checkDate(e) {
            if (e.target.value.length > 0) {
                this.setState({ submitDisabled: false });
            } else {
                this.setState({ submitDisabled: true });
            }
        }
    }, {
        key: 'render',
        value: function render() {

            var label = "";
            var labelHelp = "";
            var id = this.props.recordId;

            if (this.props.mode == "renewal") {
                label = "Renewal Date";
                labelHelp = "The date that you will need to give your 90 days notification";
            } else if (this.props.mode == "entry") {
                label = "Entry Date";
                labelHelp = "The date that you've entered Thailand";
            } else if (this.props.mode == "departure") {
                label = "Departure Date";
                labelHelp = "The date that you left Thailand";
            } else if (this.props.mode == "reported") {
                label = "Entry Date";
                labelHelp = "The date that you've given your 90 days notification";
            }

            return React.createElement(
                'div',
                { className: 'container' },
                React.createElement(
                    'form',
                    null,
                    React.createElement(
                        'div',
                        { className: 'form-group mt-4' },
                        React.createElement(
                            'label',
                            { htmlFor: 'inputEntry' },
                            label
                        ),
                        React.createElement('input', { type: 'date', className: 'form-control', id: 'dateEntry', 'aria-describedby': 'dateHelp', placeholder: 'Enter date', onChange: this.checkDate }),
                        React.createElement(
                            'small',
                            { id: 'dateHelp', className: 'form-text text-muted' },
                            labelHelp
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'container mt-4' },
                        React.createElement(
                            'div',
                            { className: 'row' },
                            React.createElement(
                                'div',
                                { className: 'col-sm  text-center' },
                                React.createElement(
                                    'button',
                                    { type: 'submit', className: 'btn btn-primary mt-3', id: 'btn_submit', 'data-id': id, disabled: this.state.submitDisabled, onClick: this.submit },
                                    'Submit'
                                )
                            ),
                            React.createElement(
                                'div',
                                { className: 'col-sm  text-center' },
                                React.createElement(
                                    'button',
                                    { type: 'submit', className: 'btn btn-secondary mt-3', id: 'btn_cancel', onClick: this.cancel },
                                    'Cancel'
                                )
                            )
                        )
                    )
                )
            );
        }
    }]);

    return Form;
}(React.Component);
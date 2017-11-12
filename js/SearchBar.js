import React, {Component} from "react";

export default class SearchBar extends Component {

    constructor(props) {
        super(props);
        this.state = {value: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(e) {
        this.setState({value: e.target.value});
    }

    handleSubmit(e) {
        this.setState({value: ''});
        this.props.loadResults(this.state.value);
        e.preventDefault();
    }

    render() {
        return (
            <div className="advance-search">
                <form onSubmit={this.handleSubmit}>
                    <div className="row">
                        <div className="input-group col-lg-10 col-md-12">
                            <input type="text" value={this.state.value} onChange={this.handleChange} className="form-control"
                                   id="search" placeholder="Search for Listings"/>
                            <span className="input-group-btn">
                                    <button className="btn btn-primary voice-button" type="button">
                                        <i className="fa fa-microphone fa-lg"></i>
                                    </button>
                            </span>
                        </div>
                        <div className="col-lg-2 col-md-12">
                                <button className="btn btn-main">SEARCH</button>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}
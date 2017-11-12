import React from 'react';

var SearchBar = React.createClass({
    render: function () {
        return (
            <div className="advance-search">
                <form action="#">
                    <div className="row">
                        <div className="input-group col-lg-10 col-md-12">
                                <input type="text" className="form-control" id="search"
                                       placeholder="Search for Listings"/>
                            <span className="input-group-btn">
                                    <button className="btn btn-primary voice-button" type="button">
                                        <i className="fa fa-microphone fa-lg"></i>
                                    </button>
                                </span>
                        </div>

                        <div className="col-lg-2 col-md-12">
                            <div className="block d-flex">
                                <button className="btn btn-main">SEARCH</button>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
});

export default SearchBar;




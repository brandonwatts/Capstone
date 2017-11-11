import React from 'react';

var SearchBar = React.createClass({
    render: function () {
        return (
            <div className="advance-search">
                <form action="#">
                    <div className="row">
                        <div className="col-lg-10 col-md-12">
                            <div className="block d-flex">
                                <input type="text" className="form-control mb-2 mr-sm-2 mb-sm-0" id="search"
                                       placeholder="Search for Listings"/>
                            </div>
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
import React from 'react';
import Listings from './Listings.js';
import SearchBar from './SearchBar.js'

var Site = React.createClass({
    render: function () {
        return (
            <div>
                <section className="hero-area bg-1 text-center overly">
                    <div className="container">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="content-block">
                                    <h1>Search for Listings Near You </h1>
                                    <p>Join the millions who buy and sell from each other <br/> everyday in local
                                        communities around the world</p>
                                </div>
                                <SearchBar/>
                            </div>
                        </div>
                    </div>
                </section>
                <Listings/>
            </div>
        );
    }
});

export default Site;
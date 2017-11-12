import React, {Component} from "react";
import Listings from './Listings.js';
import SearchBar from './SearchBar.js';
import axios from 'axios';

export default class Site extends Component {

    constructor(props) {
    super(props);
    this.loadResults = this.loadResults.bind(this);
  }

    loadResults(request){
        console.log(request);
        axios.get(`/api/nlp?request=${request}`)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {
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
                                <SearchBar loadResults={this.loadResults}/>
                            </div>
                        </div>
                    </div>
                </section>
                <Listings/>
            </div>
        );
    }
}
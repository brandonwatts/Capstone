# CoStar - Natural Language Search

CoStar Group, the nation’s largest commercial real estate information, analytics, and
marketing company, is in need of a speech recognition and natural language processing solution to be leveraged across a variety of their web and mobile products. They are requesting a REST-based API solution so that their existing products can easily take advantage of natural language processing without a need for a complete architecture.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

[Python 3.6.3](https://www.python.org/downloads/)

### Installing

Start by running the setup.py file

```
python setup.py install
```

From here all you will need is the engish model for spaCy

```
python -m spacy download en
```

## Running the tests

To test that spaCy is up and running run the following command:

```
python -m spacy validate
```

To rul all the tests (integration and unit) run the following command:

```
python run_tests.py
```

## Built With

* [Python 3.6.3](https://www.python.org/downloads/)
* [Flask](http://flask.pocoo.org/)
* [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/)
* [spaCy](https://spacy.io/)
* [marshmallow](https://marshmallow.readthedocs.io/en/latest/#)

## Authors

* **Jonathan Cary**
* **Austin Green**
* **Brandon Watts**

See also the list of [contributors](https://github.com/brandonwatts/Capstone/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/brandonwatts/Capstone/blob/master/LICENSE) file for details

## Acknowledgments

* Joshua Stickles

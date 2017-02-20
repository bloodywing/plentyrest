plenty-rest-python
===============================

version number: 0.0.1
author: Pierre Geier

Overview
--------

Python REST client for Plentymarkets REST API

Installation / Usage
--------------------

clone the repo:

    $ git clone https://github.com/bloodywing/plentyrest.git
    $ python setup.py install
    
Contributing
------------

Just send pullrequests on github or open issues.

Example
-------

    from plentyrest.rest import Plenty
    
    plenty = Plenty('myshop.plentymarkets-cloud02.com', 'restuser', 'password')
    items = plenty.request('rest/items')  # lists your items
    
    print(items)
    
    plenty.request('rest/items', 'POST', json={
        ...
        'variations': [
            {
              'name': 'Spam'
            },
        ]
    }
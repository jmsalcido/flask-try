#! /usr/bin/env python
from app import app

if __name__ == "__main__": #Need this line for Openshift
    app.run(debug=True, host='0.0.0.0', port=8051)

# microblog

a Flask experiment using the flask mega tutorial from http://blog.miguelgrinberg.com/ changing some stuff from the tutorial.

Using python 3.5, going to upload it on Openshift.

# How to

First of all, create a virtual env with python 3 and import requirements.txt from pip:

    pip install -r requirements.txt

## Run
First, run `grunt package` or:

    $ grunt package-dev
    $ python microblog/run.py

## Watch changes on microblog/assets
Just run `grunt watch` and every change will be reloaded.

## Test
Just run:

    $ python tests.py

That's all... basically.
import sys
from flask import Flask, request, jsonify, abort

import boto3
s3 = boto3.resource('s3')
s3.meta.client.download_file('bi-connections', 'bi_connections.py', '/tmp/connections.py')
sys.path.insert(1, '/tmp/')

from auxiliary_functions import get_geolocation_information, calculate_distance_between_zipcodes, find_closer_store

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def geolocation_information():
    print('<<<<<<Entrando função get_geolocation_information>>>>>')

    if request.args.get('cep') is None:
        print("No arguments")
        abort(400)

    try:
        # Getting parameter
        cep = str(request.args.get('cep'))

        print(cep)

    except Exception as e:
        print('Invalid parameter')
        print('Error message: ', e)
        abort(400)

    try:
        response = get_geolocation_information(cep=cep)

        print('response', response)

        return jsonify(response)

    except Exception as e:
        response = 'Unable to get geolocation information:'
        print(response, e)
        abort(500)


@app.route('/distance')
def distance():
    print('<<<<<<Entrando função calculate_distance_between_zipcodes>>>>>')

    try:
        # Getting parameters
        cep1 = str(request.args.get('cep1'))
        cep2 = str(request.args.get('cep2'))

    except Exception as e:
        print('Invalid parameters')
        print('Error message: ', e)
        abort(400)

    if cep1 == None or cep2 == None:
        response = "Two parameters are needed"
        print(response)
        abort(500)
    else:
        try:
            response = calculate_distance_between_zipcodes(cep1=cep1,
                                                           cep2=cep2)

            print('response', response)

            return jsonify(response)

        except Exception as e:
            response = 'Unable to calculate the distance: '
            print(response, e)
            abort(500)


@app.route('/closer')
def closer_store():
    print('<<<<<<Entrando função find_closer_store>>>>>')

    try:
        # Getting parameter
        cep = str(request.args.get('cep'))

    except Exception as e:
        print('Invalid parameter')
        print('Error message: ', e)
        abort(400)

    try:
        response = find_closer_store(cep)
        print('response', response)

        return jsonify(response)

    except Exception as e:
        response = 'Could not find the closer store: '
        print(response, e)
        abort(500)


if __name__ == '__main__':
    app.run()


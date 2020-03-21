# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:40:11 2019

@author: Bruno Caforio
"""

import math
from connections import DataWarehouseReadConnection


def get_geolocation_information(cep):
    print('<<<<<<<<<Entrou na auxiliary_functions.get_geolocation_information>>>>>>>>>>>>')

    prefix = cep[0:5]

    query = f'''select  geolocation_zip_code_prefix,
                geolocation_state,
                geolocation_city_fuzz,
                zona,
                bairros,
                regiao,
                imediate_region,
                intermediate_region,
                avg(geolocation_lat) as lat,
                avg(geolocation_lng) as lng
        from staging.geolocation_information_brazil gib
        where gib.geolocation_zip_code_prefix = '{prefix}'
        group by geolocation_zip_code_prefix,
        geolocation_city_fuzz,
        geolocation_state,
        imediate_region,
        intermediate_region,
        zona,
        bairros,
        regiao; '''

    # Entering DB
    with DataWarehouseReadConnection() as sql_conn:
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute(query)
        qry_result = sql_cursor.fetchone()

    print('qry_result', qry_result)

    # Getting results
    results = {
        'cep': cep,
        'geolocation_state': qry_result[1],
        'geolocation_city_fuzz': qry_result[2],
        'zone': qry_result[3],
        'neighborhoods': qry_result[4],
        'region_capital_SP': qry_result[5],
        'imediate_region': qry_result[6],
        'intermediate_region': qry_result[7],
        'mean_lat': float(qry_result[8]),
        'mean_lng': float(qry_result[9]),
        'google_maps_link': f'https://www.google.com/maps/@{float(qry_result[8])},{float(qry_result[9])},17z'
    }

    print('results', results)

    return results


def get_lat_lng(cep):
    print('<<<<<<<<<Entrou na auxiliary_functions.get_lat_lng>>>>>>>>>>>>')

    prefix = cep[0:5]

    query = f'''select  avg(geolocation_lat) as lat,
                        avg(geolocation_lng) as lng
              from staging.geolocation_information_brazil gib
              where gib.geolocation_zip_code_prefix = '{prefix}'; '''

    # Entering DB
    with DataWarehouseReadConnection() as sql_conn:
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute(query)
        qry_result = sql_cursor.fetchone()

    print('qry_result', qry_result)

    # Getting results
    results = {
        'mean_lat': float(qry_result[0]),
        'mean_lng': float(qry_result[1])
    }

    print('results', results)

    return results


def calculate_distance(lat1, lng1, lat2, lng2):
    rad = lambda x: x * math.pi / 180

    radlat1 = rad(lat1)
    radlat2 = rad(lat2)

    theta = lng2 - lng1
    radtheta = rad(theta)

    distance = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
    distance = math.acos(distance)
    distance = distance * 180 / math.pi
    distance = distance * 60 * 1.1515
    distance = distance * 1.609344

    return distance


def calculate_distance_between_zipcodes(cep1, cep2):
    print('<<<<<<<<<Entrou na auxiliary_functions.calculate_distance_between_zipcodes>>>>>>>>>>>>')

    lat1 = get_lat_lng(cep1)['mean_lat']
    print(lat1)
    lng1 = get_lat_lng(cep1)['mean_lng']
    print(lng1)
    lat2 = get_lat_lng(cep2)['mean_lat']
    print(lat2)
    lng2 = get_lat_lng(cep2)['mean_lng']
    print(lng2)

    distance = calculate_distance(lat1, lng1, lat2, lng2)

    results = {
        'cep1': cep1,
        'cep2': cep2,
        'approximate_distance_km': distance
    }

    return results


def find_closer_store(cep):
    print('<<<<<<<<<Entrou na auxiliary_functions.find_closer_store>>>>>>>>>>>>')

    query = '''select location_correct, 
                      location_type, 
                      latitude, 
                      longitude, 
                      location_type 
               from locations l
               where l.location_type != 'IAV' and l.longitude is not null
               group by location_correct, location_type, latitude, longitude; '''

    # Entering DB - getting stores
    with DataWarehouseReadConnection() as sql_conn:
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute(query)
        qry_result = sql_cursor.fetchall()

    # Getting lat and lng of the given zipcode
    lat_lng_cep = get_lat_lng(cep)
    stores_distances = list()

    for store in qry_result:
        stores_distances.append(calculate_distance(lat_lng_cep['mean_lat'],
                                                   lat_lng_cep['mean_lng'],
                                                   store[2],
                                                   store[3]))

    results = {
        'cep': cep,
        'closer_store': qry_result[stores_distances.index(min(stores_distances))][0],
        'approximate_distance_km': min(stores_distances),
        'store_lat': qry_result[stores_distances.index(min(stores_distances))][2],
        'store_lng': qry_result[stores_distances.index(min(stores_distances))][3],
        'store_type': qry_result[4][4]
    }

    return results
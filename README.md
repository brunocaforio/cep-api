# CEP API Prototype

This Prototype provides an API that returns geolocation information to the user for a given zipcode.
I've designed it as my first project in my first job. The company needed a service that with a given zipcode, we could find some interesting geolocation information. 
This had the purpose of beeing used during the scheduling of an appointment by our client to find the closer store. This was also used in geolocation analysis about the regions and neighbors that had the major demand of our services, giving a basis for logistic decisions of the company. 

This prototype has three services that can be accessed:
```
    - Return geolocation information given a unique zipcode (zipcode, geolocation_state, geolocation_city_fuzz, zone, neighborhoods, region_capital_SP, imediate_region, intermediate_region, mean_lat, mean_lng and google_maps_link);
        - Parameter: cep
        - Output description:
            - zipcode: the same zipcode that was passed as parameter to the API;
            - geolocation_state: the Brazil state related to the given zipcode;
            - geolocation_city_fuzz: name of the city. The sufix 'fuzz' relates to the fact that the name was produced by FuzzyWuzzy string matching. Some cities out of big São Paulo may be with incorrect name in this current prototype;
            - zone: zone of the city;
            - neighborhoods: neighborhoods that are close to the given zipcode;
            - region_capital_SP: region of the capital of SP;
            - imediate_region: imediate region of the state;
            - intermediate_region: intermediate region of the state;
            - mean_lat: mean latitude;
            - mean_lng: mean longitude;
            - google_maps_link: google maps link for the current zipcode.
 
    - Return the mean linear distance (in kilometers) between two zipcodes;
        - Parameter: cep1 and cep2
        - Output description:
            - cep1: the first zipcode that was passed as parameter;
            - cep2: the second zipcode that was passed as parameter;
            - approximate_distance_km: the calculated mean linear distance between the zipcodes.

    - Return the closer store to a given zipcode and the mean linear distance (in kilometers), besides the store latitude and longitude;
        - Parameter: cep
        - Output description:
            - cep: the zipcode that was passed as parameter;
            - closer_store: the name of the closer Instacarro store to the given zipcode;
            - approximate_distance_km: the mean linear distance calculated between the given zipcode and the closer store that was returned;
            - store_lat: the latitude of the closer store;
            - store_lng: the longitude of the closer store;
            - store_type: the type of the store ('Loja Propria', 'Parceiro' or 'Docking').
```

## Data used
This API uses the data that is in the csv file inside "database" directory. Those data were extracted from kaggle and some pre-processing procedures were required like the use of fuzzywuzzy package to correct the name of some states.
The database has the mean latitude and longitude for each zipcode prefix. 

Besides that, another database is consulted in the code to get the closer store. This consulting is made inside the function 'find_closer_store' in auxiliary_functions module.


## Examples of usage and outputs

```
    - Using zipcode to get geolocation information:
        GET: https://{AWS-API-GATEWAY}?cep=09210700
        - output: {"cep":"09210700","geolocation_state":"SP","geolocation_city_fuzz":"Santo André","zone":"NULL","neighborhoods":"NULL","region_capital_SP":"NULL","imediate_region":"São Paulo","intermediate_region":"São Paulo","mean_lat":-23.63738184885248,"mean_lng":-46.528097878610865,"google_maps_link":"https://www.google.com/maps/@-23.63738184885248,-46.528097878610865,17z"}

        Note: if "NULL" is returned for "bairros", "regiao" and/or "zona", the given zipcode doesn't refer to São Paulo city

    - Using two zipcodes to calculate the mean linear distance:
        GET: https://{AWS-API-GATEWAY}/distance?cep1=09210700&cep2=09080510
        - output: {"cep1":"09210700","cep2":"09080510","approximate_distance_km":1.430901608053396}

        Note: the distance returned by Google Maps between these two zipcodes is, approximately, 2.1 km

    - Using one zipcode to get the closer store:
        GET: https://{AWS-API-GATEWAY}/closer?cep=09210700
        - output: {"cep":"09210700","closer_store":"Extra São Caetano","approximate_distance_km":5.76890252237499,"store_lat":-23.615031,"store_lng":-46.579204,"store_type":"Loja Propria"}
```

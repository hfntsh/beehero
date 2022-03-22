from collections import OrderedDict
import flask
from flask import request
import json
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast, asc, desc

from base import Base, Session, engine
from city import City
from forecast import Forecast


app = flask.Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/avg_tmp_per_city_per_day', methods=['GET'])
def avg_tmp_per_city_per_day():
    """
    avg_tmp_per_city_per_day
    Calculates, for each city, for each day, its average temperature.
    :return: a string representation of a JSON, mapping from city to a map from day to average temperature.
    """
    session = Session()
    cities = session.query(City.id, City.name).all()
    # Maps from city to a map of day to average temp.
    result_dict = {}
    # There might be some more elegant query, but this works.
    for city_id, city_name in cities:
        city_average = session.query(
            Forecast.date, func.round(func.avg(cast(Forecast.temperature, sqlalchemy.Numeric)),1)
        ).filter(Forecast.city_id == city_id).group_by(Forecast.date).all()
        result_dict[city_name] = dict(city_average)
        # To JSONify later, we need all keys to be strings rather than datetime.time,
        # and values to be float rather than Decimal
        for key, value in result_dict[city_name].items():
            del result_dict[city_name][key]
            result_dict[city_name][str(key)] = float(value)
    session.close()
    return json.dumps(result_dict)


@app.route('/lowest_humid', methods=['GET'])
def lowest_humid():
    """
    lowest_humid
    Finds the absolute lowest humidity values in the database. Returns it together with the city, date and time when
    it occured.
    :return: a string representation of a JSON, containing city name, date, time, and humidity value.
    """
    session = Session()
    # To find minimum humidity point and time we sort by ascending humidity and take the first value.
    # This is kind of a heavy query, unsure how to optimize.
    query = session.query(
        Forecast.city_id, Forecast.date, Forecast.time, Forecast.humidity
    ).order_by(asc(Forecast.humidity)).limit(1).all()
    city_id = query[0][0]
    date = query[0][1]
    time = query[0][2]
    humidity = query[0][3]
    city = session.get(City, city_id)
    result_list = [city.name, str(date), str(time), humidity]
    session.close()
    return json.dumps(result_list)


@app.route('/feels_like_rank', methods=['GET'])
def feels_like_rank():
    """
    feels_like_rank
    returns a sorted dict of cities, with the latest feels like, and sorted. Sorting defaults to ascending order, unless
    url param order_dir is set to "asc".
    :return: a string representation on JSON, mapping each city to its feels like, sorted by feels like.
    """
    session = Session()
    # We default to ascending order, and do not fail in case we get a parameter which isn't "asc" or "desc".
    order_dir = request.args.get("order_dir", default="asc")
    reverse_order = order_dir == "desc"
    cities = session.query(City.id, City.name).all()
    result_dict = {}
    for city_id, city_name in cities:
        query = session.query(
            Forecast.city_id, Forecast.date, Forecast.time, Forecast.feels_like
        ).filter(Forecast.city_id == city_id).order_by(desc(Forecast.date)).order_by(desc(Forecast.time)).limit(1).all()
        result_dict[city_name] = query[0][3]
    ordered_result = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1], reverse=reverse_order))
    session.close()
    return json.dumps(ordered_result)


app.run()

import flask

# TODO: Types!
# TODO: unit tests
# TODO: DB connection

# TODO:
# set up DB + schema
# get data loaders to work with DB
# load data
# create magic script that sets up DB and loads data
# do the server side
# dockerize it all
# create instructions etc.
# also unit tests probably

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/avg_tmp_per_city_per_day', methods=['GET'])
def avg_tmp_per_city_per_day():
    return "So you want avg tmp per city per day, huh?"


@app.route('/lowest_humid', methods=['GET'])
def lowest_humid():
    return "So you want lowest humid, huh?"


@app.route('/feels_like_rank', methods=['GET'])
def feels_like_rank():
    return "So you want a rank by feels like, huh?"


app.run()

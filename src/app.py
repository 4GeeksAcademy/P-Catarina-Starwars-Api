"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# USERS ROUTES
@app.route('/users', methods=['GET'])
def get_table_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    if len(users) == 0:
        return "Users table is empty", 400
    return jsonify(users), 200

# FAVORITES ROUTES
@app.route('/favorites/users', methods=['GET'])
def get_table_favorites():
    favorites = Favorites.query.all()
    favorites = list(map(lambda fav: fav.serialize(), favorites))
    if len(favorites) == 0:
        return "Favorites table is empty", 400
    return jsonify(favorites), 200

@app.route('/favorites/user-<int:id_user>', methods=['GET'])
def get_user_favorites(id_user):
    favorites = Favorites.query.filter_by(id_user = id_user).all()
    favorites = list(map(lambda fav: fav.serialize(), favorites))
    if len(favorites) == 0:
        return "This user doesn't exist or has no favorites yet", 400
    return jsonify(favorites), 200

@app.route('/favorites/user-<int:id_user>/planet-<int:id_planet>', methods=['POST'])
def add_favorite_planet(id_user, id_planet):
    if User.query.get(id_user) is None:
        return "This user doesn't exist", 400
    
    if Planets.query.get(id_planet) is None:
        return "This planet doesn't exist", 400
    
    match = Favorites.query.filter_by(id_user = id_user, id_planet = id_planet).all()
    if len(match) is not 0:
        return "Already in the database", 400

    new_fav = Favorites(
        id_planet = id_planet, 
        id_user = id_user,
    )

    db.session.add(new_fav)
    db.session.commit()
    return "Planet added to Favorites", 200

@app.route('/favorites/user-<int:id_user>/people-<int:id_person>', methods=['POST'])
def add_favorite_person(id_user, id_person):
    if User.query.get(id_user) is None:
        return "This user doesn't exist", 400
    
    if People.query.get(id_person) is None:
        return "This person doesn't exist", 400
    
    match = Favorites.query.filter_by(id_user = id_user, id_person = id_person).all()
    if len(match) is not 0:
        return "Already in the database", 400

    new_fav = Favorites(
        id_person = id_person, 
        id_user = id_user,
    )

    db.session.add(new_fav)
    db.session.commit()
    return "Person added to Favorites", 200

@app.route('/favorites/user-<int:id_user>/planet-<int:id_planet>', methods=['DELETE'])
def delete_favorite_planet(id_user, id_planet):
    if User.query.get(id_user) is None:
        return "This user doesn't exist", 400
    
    if Planets.query.get(id_planet) is None:
        return "This planet doesn't exist", 400
    
    match = Favorites.query.filter_by(id_user = id_user, id_planet = id_planet).first()
    if match is None:
        return "Not in Favorites", 400

    db.session.delete(match)
    db.session.commit()
    return "Planet removed from Favorites", 200

@app.route('/favorites/user-<int:id_user>/people-<int:id_person>', methods=['DELETE'])
def delete_favorite_person(id_user, id_person):
    if User.query.get(id_user) is None:
        return "This user doesn't exist", 400
    
    if People.query.get(id_person) is None:
        return "This person doesn't exist", 400
    
    match = Favorites.query.filter_by(id_user = id_user, id_person = id_person).first()
    if match is None:
        return "Not in Favorites", 400

    db.session.delete(match)
    db.session.commit()
    return "Person removed from Favorites", 200

# CHARACTERS ROUTES
@app.route('/people', methods=['GET'])
def get_table_people():
    people = People.query.all()
    people = list(map(lambda person: person.serialize(), people))
    if len(people) == 0:
        return "People table is empty", 400
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    person = person.serialize()
    if person is None:
        return "This person doesn't exist", 400
    return jsonify(person), 200

# PLANETS ROUTES
@app.route('/planets', methods=['GET'])
def get_table_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    if len(planets) == 0:
        return "Planets table is empty", 400
    return jsonify(planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    planet = Planets.query.get(planets_id)
    planet = planet.serialize()
    if planet is None:
        return "This planet doesn't exist", 400
    return jsonify(planet), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
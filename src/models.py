from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "description": self.description
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_person = db.Column(db.Integer, db.ForeignKey('people.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('planets.id'))

    user = db.relationship(User)
    people = db.relationship(People)
    planets = db.relationship(Planets)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        if self.id_person is not None:
            return {
                "id": self.id,
                "user": self.id_user,
                "person": self.id_person,
            }
    
        if self.id_planet is not None:
            return {
                "id": self.id,
                "user": self.id_user,
                "planet": self.id_planet
            }
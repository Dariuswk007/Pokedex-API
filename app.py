from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
CORS = (app)
ma = Marshmallow(app)

class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dex_entry = db.Column(db.String, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __init__(self, name, dex_entry, height, weight):
        self.name = name
        self.dex_entry = dex_entry
        self.height = height
        self.weight = weight

class PokedexSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'dex_entry', 'height', 'weight')

pokedex = PokedexSchema()
pokedexes = PokedexSchema(many=True)

@app.route('/pokedex/add', methods=['POST'])
def add_entry():
    post_data = request.get_json()
    name = post_data.get('name')
    dex_entry = post_data.get('dex_entry')
    height = post_data.get('height')
    weight = post_data.get('weight')

    new_entry = Pokedex(name, dex_entry, height, weight)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify("You have added a new Pokemon entry!")

@app.route('/pokedex/get', methods=['GET'])
def get_entry():
    entries = db.session.query(Pokedex).all()
    return jsonify(pokedexes.dump(entries))


@app.route('/pokedex/delete/<id>', methods=['DELETE'])
def delete_entry():
    pokemon = db.session.query(Pokedex).filter(Pokedex.id == id).first()
    



if __name__ == "__main__":
        app.run(debug=True)
    
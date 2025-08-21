from flask import Flask, jsonify, request
from models import db, People, Planet, User, Favorites

app = Flask(__name__)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize())
    return jsonify({"error": "Person not found"}), 404

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    return jsonify({"error": "Planet not found"}), 404

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter(
        (Favorites.favorite_people_id != None) | (Favorites.favorite_planet_id != None)
    ).all()
    user_favorites = []
    for fav in favorites:
        fav_data = fav.serialize()
        if fav.favorite_people_id:
            fav_data["people"] = People.query.get(fav.favorite_people_id).serialize()
        if fav.favorite_planet_id:
            fav_data["planet"] = Planet.query.get(fav.favorite_planet_id).serialize()
        user_favorites.append(fav_data)
    return jsonify(user_favorites)

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def post_user_favorite_planet(user_id, planet_id):
    favorite = Favorites(favorite_planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def post_user_favorite_people(user_id, people_id):
    favorite = Favorites(favorite_people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_user_favorite_planet(user_id, planet_id):
    favorite = Favorites.query.filter_by(favorite_planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite planet deleted"})
    return jsonify({"error": "Favorite not found"}), 404

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_user_favorite_people(user_id, people_id):
    favorite = Favorites.query.filter_by(favorite_people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite people deleted"})
    return jsonify({"error": "Favorite not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
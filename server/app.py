#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants")
def restaurants():
    restaurants = Restaurant.query.all()
    restaurantslist=[restaurant.to_basic_dict() for restaurant in restaurants]
    return make_response(restaurantslist, 200)
   
@app.route("/restaurants/<int:id>", methods=['GET','DELETE'])
def restaurantbyid(id):
    restaurant = Restaurant.query.filter(Restaurant.id== id).first()

    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    if request.method== 'GET':
        return make_response(restaurant.to_dict(), 200)

    elif request.method=='DELETE':
        db.session.delete(restaurant)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        response = make_response(
            response_body,
            204
        )

        return response 


@app.route("/pizzas")
def pizzas():
    pizzas = Pizza.query.all()
    pizzaslist=[pizza.to_dict() for pizza in pizzas]
    return make_response(pizzaslist, 200)


@app.route("/restaurant_pizzas", methods=['POST'])
def restaurants_pizzas():
    data = request.json
    try:
        respiz = RestaurantPizza(price= data['price'], pizza_id=data['pizza_id'], restaurant_id= data['restaurant_id'])
        db.session.add(respiz)
        db.session.commit()
        return make_response(respiz.to_dict(), 201)
    except ValueError as e:
        return make_response({"errors": ["validation errors"]}, 400)



if __name__ == "__main__":
    app.run(port=5555, debug=True)

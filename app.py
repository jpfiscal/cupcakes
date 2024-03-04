"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

def serialize_cupcakes(cupcake):
    """convert cupcake object into JSON compatible dictionary object"""

    return{
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/")
def view_home():
    """Render home page"""
    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)

@app.route("/api/cupcakes")
def get_cupcakes():
    """Return list of all cupcakes in db"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcakes(c) for c in cupcakes]

    return jsonify(cupcakes = serialized)

@app.route("/api/cupcakes", methods=["POST"])
def make_cupcake():
    """Create new cupcake. This will return a JSON object for the new 
    cupcake object in the following JSON format: {id, flavor, size, rating, image}
    """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcakes(new_cupcake)

    #Return JSON object with status code 201
    return ( jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Return details of a selected cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcakes(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Update existing cupcake record"""

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake = serialize_cupcakes(cupcake))

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete a selected cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
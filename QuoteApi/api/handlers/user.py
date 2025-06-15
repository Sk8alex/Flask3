from api import app, db
from api.models.user import UserModel
from flask import abort, jsonify, request
from api.schemas.user import user_schema
from marshmallow import ValidationError
from api.schemas.user import user_schema, UserSchema


@app.get('/users/<int:user_id>') #зефирка
@app.output(UserSchema)
@app.doc(summary="Get user by id", description="Get user by id", tags=["users"])
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description=f"User with id={user_id} not found")
    return user,200



# def get_user_by_id(user_id: int):
#     pass


@app.get("/users")
@app.output(UserSchema(many=True))
@app.doc(summary="Get all user", description="Get all user", tags=["users"])
def get_users(): #зефирка
    users = db.session.scalars(db.select(UserModel)).all()
    return users, 200



# def get_users():users
#     pass

@app.post("/users")
def create_user():
    """ Function creates new quote and adds it to db."""
    data = request.json
    try:
        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <username> and <password>. Received: {', '.join(data.keys())}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    
    return jsonify(user_schema.dump(user)), 201


# url:  /users - POST
@app.post("/users1")
def create_user1():
    try:
        user = user_schema.loads(request.data)
        user.save()
    except ValidationError as ve:
        abort(400, f"Validation error: {ve.messages_dict}")
    
    return jsonify(user_schema.dump(user)), 201


# def create_user():
#     pass


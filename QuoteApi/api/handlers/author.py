from marshmallow import ValidationError, EXCLUDE
from api import db, app, token_auth
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, change_author_schema, AuthorSchema, MessageOut

@app.post("/authors")
@token_auth.login_required
def create_author():
    try:
        # 1. Get raw bytes
        # print(f'{request.data =})
        # 2. Load bytes to dict
        # author_data = author_schema.loads(request.data)
        # print(f'{author_data = }, {type(author_data)})
        # 3. Create new AuthorModel instance via dict
        # author = AuthorModel(**author_data)
        author = author_schema.loads(request.data)  # get_data() return raw bytes
        db.session.add(author)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f"Validation error: {str(ve)}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    # db instance -> dict -> json
    return jsonify(author_schema.dump(author)), 201


@app.post("/authors_api")
@app.auth_required(token_auth)
@app.input(AuthorSchema, arg_name="author")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Create new author", description="Create new author", responses=[503], tags=["Authors"])
def create_author_api(author):
    try:
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    # db instance -> dict -> json
    return author



# @app.post("/authors1")
# def create_author1():
#     author_data = request.json
#     try:
#         if not all(key in author_data for key in ["name", "surname"]):
#             raise TypeError("Missing required fields: name and surname")
#         author = AuthorModel(**author_data)
#         db.session.add(author)
#         db.session.commit()
#     except TypeError as te:
#         abort(400, f"Invalid data. Required fields: name, surname. Received: {', '.join(author_data.keys())}. Error: {str(te)}")
#     except Exception as e:
#         abort(503, f"Database error: {str(e)}")
#     return jsonify(author.to_dict()), 201


@app.get("/authors_all_api")
@app.auth_required(token_auth)
@app.output(AuthorSchema(many=True))
@app.doc(summary="Get all authors", description="Get all authors", tags=["Authors"])
def get_authors_api():
    return db.session.scalars(db.select(AuthorModel)).all(), 200


# @app.get("/authors_api")
# def get_authors_api(): #зефирка
#     authors = db.session.scalars(db.select(AuthorModel)).all()
#     return jsonify(author_schema.dump(authors, many=True)), 200

# @app.get("/authors")
# def get_authors():
#     authors_db = db.session.scalars(db.select(AuthorModel)).all()
#     authors = [author.to_dict() for author in authors_db]
#     return jsonify(authors), 200


@app.get('/authors/<int:author_id>') #зефирка
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    return jsonify(author_schema.dump(author)),200

# @app.get('/authors/<int:author_id>')
# def get_author_by_id(author_id: int):
#     author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
#     # instance -> dict -> json
#     return jsonify(author.to_dict()), 200

@app.put("/authors/<int:author_id>")
@token_auth.login_required
def edit_authors(author_id: int):
    """ Update an existing quote """
    try:
        new_data = change_author_schema.load(request.json, unknown=EXCLUDE) # get_json() -> need load
    except ValidationError as ve:
        return abort(400, f"Validation error: {str(ve)}.")
    
    # Проверка на пустой словарь, т.е. есть данные для обновления
    if not new_data: # check that new_data is not {}
        return abort(400, "No valid data to update.")

    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in new_data.items():
            setattr(author, key_as_attr, value)

        db.session.commit()
        return jsonify(author_schema.dump(author)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
        
# @app.put("/authors/<int:author_id>")
# def edit_authors(author_id: int):
#     """ Update an existing quote """
#     try:
#         new_data = change_author_schema.load(request.json,
#                                     unknown=EXCLUDE) #get json > need format
#     except ValidationError as ve:
#         return abort(400, f"Invalid data to update: {str(ve)}")

#     # Проверка на пустой словарь, т.е. есть данные для обновления
#     if not new_data: # check that new_data is not {}
#         return abort(400, "No valid data to update.")

#     author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

#     try:
#         for key_as_attr, value in new_data.items():
#             # Проверка на лишние ключи(атрибуты)
#             if not hasattr(author, key_as_attr):
#                 abort(400, f"Invalid key='{key_as_attr}'. Valid only 'name' and 'surname'")
#             setattr(author, key_as_attr, value)

#         db.session.commit()
#         return jsonify(author_schema.dump(author)), 200
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    """Delete author by id """
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Author with id {author_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors_api/<int:author_id>")
@app.auth_required(token_auth)
@app.output(MessageOut)
@app.doc(summary="Delete author by id", description="Delete author by id", tags=["Authors"], responses=[503])
def delete_author_api(author_id):
    """Delete author by id """
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return {"message": f"Author with id {author_id} has deleted."}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
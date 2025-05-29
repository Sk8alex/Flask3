from api import db, app
from flask import request, abort, jsonify
#from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from . import check
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError

@app.post("/authors")
def create_author():
    author_data = request.json
    try:
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <name>. Received: {', '.join(author_data.keys())}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author.to_dict()), 201


@app.get("/authors")
def get_authors():
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    authors = [author.to_dict() for author in authors_db]
    return jsonify(authors), 200


@app.get('/authors/<int:author_id>')
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # instance -> dict -> json
    return jsonify(author.to_dict()), 200


@app.put("/authors/<int:author_id>")
def edit_authors(author_id: int):
    """ Update an existing quote """
    new_data = request.json
    result = new_data
    # if not result[0]:
    #     return abort(400, result[1].get('error'))
    
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in new_data.items():
            setattr(author, key_as_attr, value)

        db.session.commit()
        return jsonify(author.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.route("/authors/<int:author_id>", methods=['DELETE'])
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
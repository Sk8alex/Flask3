from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


#Example of custom validator
def rating_validate(value: int):
    # if return True-> validation success
    # if return False - > raise ValueError
    return value in range(1, 6)

class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        #load_instance = True

    id = ma.auto_field()
    text = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("name")))
    rating = ma.Integer(strict=True, valadate=rating_validate)


quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)
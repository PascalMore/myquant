from flask_restplus import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required
from .serializers import article_list
from .models import ArticleList

api = Namespace('article', 'Daily Market Report')

@api.route('/list')
class Article(Resource):
    @api.marshal_with(article_list)
    @api.response(404, 'Article not found')
    @jwt_required
    def get(self):
        """
        Get all articles
        """
        articles = ArticleList.get_article_list()
        if articles is not None:
            return articles
        else:
            api.abort(404, 'Article not found')
        
@api.route('/create')
class Article(Resource):
    @api.marshal_with(article_list)
    @api.response(500, 'Article create failed')
    @jwt_required
    def post(self):
        """
        Create an article
        """
        res = ArticleList.create_article(api.payload)
        if res == 0:
            return {'message': 'Save article successfull'}
        else:
            api.abort(500, 'Save article failed')

from flask import Blueprint
from flask_restplus import Api

v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(v1_blueprint,
          doc='/docs',
          title='Flask App',
          version='1.0',
          description='Flask RESTful API',
          security='Bearer Auth',
          authorizations=authorizations)

from .resources.auth.login import api as auth_ns
from .resources.users.user import api as user_ns
from .resources.labels.label_arch import api as label_arch_ns
from .resources.labels.asset_label import api as asset_label_ns
from .resources.stocks.stock import api as stock_list_ns
from .resources.strategy.strategy_execution import api as strategy_ns
from .resources.diary.article import api as article_ns
from .resources.indicator.indicator import api as indicator_ns
from .resources.stockpool.stockpool import api as stock_pool_ns
from .resources.stocknotice.stocknotice_adv import api as stock_notice_adv_ns
from .resources.index.index import api as index_ns


api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(label_arch_ns)
api.add_namespace(asset_label_ns)
api.add_namespace(stock_list_ns)
api.add_namespace(strategy_ns)
api.add_namespace(article_ns)
api.add_namespace(indicator_ns)
api.add_namespace(stock_pool_ns)
api.add_namespace(stock_notice_adv_ns)
api.add_namespace(index_ns)
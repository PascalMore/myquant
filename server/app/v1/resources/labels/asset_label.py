from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import asset_label
from .models import AssetLabels


api = Namespace('asset_label', 'Asset Label Endpoint')

@api.route('/arch/<string:arch_name>/assetid/<string:aid>/date/<string:date>')
class LabelArch(Resource):
    @api.marshal_with(asset_label)
    @api.response(404, 'Asset label not found')
    @api.doc(params={'arch_name': 'Label Arch Name', 'aid': 'Asset ID', 'date': 'Query Date'})
    @jwt_required
    def get(self, arch_name, aid, date):
        """
        Get asset label by asset id of query date
        """
        asset_label = AssetLabels.get_label_by_id(arch_name, aid, date)
        if not asset_label:
            api.abort(404, 'Asset label not found')
        return asset_label

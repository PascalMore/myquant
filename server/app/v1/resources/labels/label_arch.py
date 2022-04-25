from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import label_arch
from .models import LabelArchs


api = Namespace('label_arch', 'Label Arch Endpoint')

@api.route('/<string:arch_name>')
class LabelArch(Resource):
    @api.marshal_with(label_arch)
    @api.response(404, 'Label arch not found')
    @api.doc(params={'arch_name': 'Label arch Name'})
    @jwt_required
    def get(self, arch_name):
        """
        Get label arch by Name
        """
        label_arch = LabelArchs.get_labelarch_by_name(arch_name)
        if not label_arch:
            api.abort(404, 'Label arch not found')
        return label_arch

@api.route('/list/<string:arch_type>')
class LabelArch(Resource):
    @api.marshal_with(label_arch)
    @api.response(404, 'Label arch not found')
    @api.doc(params={'arch_type': 'Label arch Type'})
    @jwt_required
    def get(self, arch_type):
        """
        Get all arch by type
        """
        label_arch = LabelArchs.get_all_labelarch(arch_type)
        if not label_arch:
            api.abort(404, 'Label arch not found')
        return label_arch

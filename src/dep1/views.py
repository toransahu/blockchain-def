from rest_framework import viewsets, mixins
from .models import Scheme
from .serializers import SchemeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.multichain_api import api, publish_stream, get_tx_data
from utils import hex_to_json
from uuid import uuid4

# Create your views here.

class SchemeViewSet(viewsets.ModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer


@api_view(['POST'])
def make_request(request):
    data = request.data
    stream = 'scheme'
    _ticket_no = 1  #TODO: get it from Ticket Model using prefetch_id() 
    _from = 'dep1'
    _to = 'dep2'  #TODO: get it from request.data
    key = f'{_from}-{_to}-{_ticket_no}'
    data_to_publish = ''  #TODO: get it from request.data
    txid = publish_stream(stream, key, data_to_publish, data_format='json')
    
    if txid:
        # TODO: define notify()
        notify(_from, _to, _ticket_no, txid, stream, key)
    else:
        pass  # inform user about failure


@api_view(['POST'])
def load_data(request):
    data = request.data
    txid = ''  # TODO: get it from notification/table 
    tx_data = get_tx_data(txid)
    json_data = hex_to_json(tx_data)
    d = json.loads(str(json_data))
    if isinstance(d, list):
        for data in d:
            aadhar = d["aadhar_number"]
            count = Scheme.objects.filter(aadhar_number=aadhar).count()
            if count > 0:
                obj = Scheme.objects.get(aadhar)
                obj.beneficiary_name = d["beneficiary_name"]
                obj.address = d["address"]
                obj.gender = d["gender"]
                obj.member_age = d["member_age"]
                obj.dist_name = d["dist_name"]
                obj.scheme_name = d["scheme_name"]
                obj.save()
    else:
        aadhar = d["aadhar_number"]
        count = Scheme.objects.filter(aadhar_number=aadhar).count()
        if count > 0:
            obj = Scheme.objects.get(aadhar)
            obj.beneficiary_name = d["beneficiary_name"]
            obj.address = d["address"]
            obj.gender = d["gender"]
            obj.member_age = d["member_age"]
            obj.dist_name = d["dist_name"]
            obj.scheme_name = d["scheme_name"]
            obj.save()



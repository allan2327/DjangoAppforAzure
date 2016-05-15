from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
import json
from reportlab.pdfgen import canvas
import urllib2
# Create your views here.

def index(request):
    args = {}
    args.update(csrf(request))
    return render(request, 'index.html')


def predict(request):
    if request.method == "POST":
        Age = request.POST.get('Age')
        Education = request.POST.get('Education')
        Education_num = request.POST.get('Education_num')
        Martial_Status = request.POST.get('Martial_Status')
        Relationship = request.POST.get('Relationship')
        Race = request.POST.get('Race')
        Sex = request.POST.get('Sex')
        Capital_gain = request.POST.get('Capital_gain')
        Capital_loss = request.POST.get('Capital_loss')
        Hours_per_week = request.POST.get('Hours_per_week')

        data_list = []

        data_list.append(str(Age))
        data_list.append(str(Education))
        data_list.append(str(Education_num))
        data_list.append(str(Martial_Status))
        data_list.append(str(Relationship))
        data_list.append(str(Race))
        data_list.append(str(Sex))
        data_list.append(str(Capital_gain))
        data_list.append(str(Capital_loss))
        data_list.append(str(Hours_per_week))


        data = {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["age", "education", "education-num", "marital-status", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week"],
                        "Values": [data_list,  ]
                    },},
                "GlobalParameters": {
        }
        }

        body = str.encode(json.dumps(data))

        url = 'https://ussouthcentral.services.azureml.net/workspaces/8a7dce9ff8034885abaec4501f06f5db/services/32a748a0efc64da4954f2d19296d2dbf/execute?api-version=2.0&details=true'
        api_key = '1d8OnzUh7lAxunjVyPmWsZVmHU+zA8crGuqROEsFJj1rfX1FedeBZTrnHtTiSV0fyy6dM1lXil7KQPwlkthKJg=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib2.Request(url, body, headers)

        try:
            response = urllib2.urlopen(req)
            result = json.loads(response.read())
            print result['Results']
            for i in result['Results']:
                for j in result['Results'][i]:
                    for k in result['Results'][i][j]:
                        if k=="Values":
                            res = result['Results'][i][j][k][0][0]
                            return HttpResponse("Predicted Score is: "+res)
            #for line in result['Results']:
        except urllib2.HTTPError, error:
            print("The request failed with status code: " + str(error.code))
            print(error.info())
            print(json.loads(error.read()))

    return HttpResponse(result)

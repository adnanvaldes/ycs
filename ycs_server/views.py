from django.shortcuts import render, HttpResponse
from .serializer import SuntimesSerializer
from ycs_server.models import SunTimes, UserSettings
from rest_framework import viewsets
import requests


class SuntimesViewset(viewsets.ModelViewSet):
	serializer_class = SuntimesSerializer

	def get_queryset(self):
		data = SunTimes.objects.all()
		return data

	def _get_suntimes(self):
		url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0'
		api_request = requests.get(url)

		try:
			api_request.raise_for_status()
			return api_request.json()
		except:
			return None

def index(request):
	return HttpResponse("Hello world!")
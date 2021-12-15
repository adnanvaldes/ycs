from rest_framework import serializers
from .models import SunTimes

class SuntimesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SunTimes
		fields = ['timestamp',
				  'date',
				  'sunrise',
				  'sunset',
				  'solar_noon',
				  'day_length',
				  'civil_twilight_start',
				  'civil_twilight_end',
				  'nautical_twliglight_start',
				  'nautical_twilight_end',
				  'astronomical_twilight_start',
				  'astronomical_twilight_end']
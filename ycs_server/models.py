from django.db import models


# Create your models here.

class UserSettings(models.Model):
	on_transition = models.IntegerField()
	off_transition = models.IntegerField()
	lat = models.FloatField()
	lng = models.FloatField()
	morning = models.TimeField()
	evening = models.TimeField()
	ping_bulb_freq = models.IntegerField()

	def __str__(self):
		return f"Current settings:\nMorning: {self.morning}\nEvening: {self.evening}\nOn Transition:{self.on_transition}\nOff Transition: {self.off_transition}"


class SunTimes(models.Model):
	date = models.DateField(auto_now_add=True)
	timestamp = models.TimeField(auto_now_add=True)
	sunrise = models.TimeField()
	sunset = models.TimeField()
	solar_noon = models.TimeField()
	day_length = models.TimeField()
	civil_twilight_start = models.TimeField()
	civil_twilight_end = models.TimeField()
	nautical_twilight_start = models.TimeField()
	nautical_twilight_end = models.TimeField()
	astronomical_twilight_start = models.TimeField()
	astronomical_twilight_end = models.TimeField()

	def __str__(self):
		return f"[{self.timestamp}]: {self.date} - Sunrise:{self.sunrise}, Sunset:{self.sunset}"
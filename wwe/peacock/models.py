from django.db import models

class Location(models.Model):
	name = models.CharField(max_length=500)

class Venue(models.Model):
	name = models.CharField(max_length=500)
	location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)

class Match(models.Model):
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

class Performer(models.Model):
	name = models.CharField(max_length = 500)

class EventName(models.Model):
	name = models.CharField(max_length=500)

class Event(models.Model):
	name = models.ForeignKey(EventName, on_delete=models.CASCADE)
	date = models.DateField()
	venue = models.ForeignKey(Venue, null=True, on_delete=models.SET_NULL)


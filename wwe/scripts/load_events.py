from peacock.models import Location, Venue, Match, Performer, EventName, Event

import json, re
from datetime import datetime

def run():
	f = open('../wwe_event_data.txt')
	event_data = json.load(f)

	for event in event_data:
		e_n, created = EventName.objects.get_or_create(name=event['title'])
		loc, created = Location.objects.get_or_create(name=event['City'])
		ven, created = Venue.objects.get_or_create(name='Venue',location=loc)
		d = event['Date'].replace('\xa0', ' ')
		d = d.rstrip(", ")
		
		try:
			d = datetime.strptime(re.split('\[|(\, \()',d)[0], '%B %d, %Y')
		except:
			d = datetime.strptime(re.split('\[|(\, \()',d)[0], '%d %B %Y')
		e, created = Event.objects.get_or_create(name=e_n,date=d,venue=ven)
		
		for match in event['matches']:
			for c in match['competitors']:
				performer, created = Performer.objects.get_or_create(name=c)
				print(performer)
		print(e)

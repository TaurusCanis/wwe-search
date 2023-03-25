from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/List_of_WWE_pay-per-view_and_WWE_Network_events#Past_events"

base_url = "https://en.wikipedia.org"

# page = requests.get(url)

file = open('wikipedia_event_list.html', 'r')
soup = BeautifulSoup(file, 'html.parser')

event_detail_list = []

#event_list = soup.find_all('th', text='Current')[1].next_sibling.find_all('a')
#event_list = soup.find('span', id='1985').parent.next_siblings

e = soup.find('span', id='1985').parent.next_sibling.next_sibling

import time

def get_event_detail(a):
	print("******CALLING*******: ", a)
	time.sleep(2)
	event_page = requests.get(base_url + a)
	event_data = {}
	matches = []

	###print(event_page.text)
	###print(event_page.text)
	event_detail_soup = BeautifulSoup(event_page.text, 'html.parser')
	infobox_data = event_detail_soup.find('table', class_='infobox').next_element.contents

	title = infobox_data[0].next_element.next_element.string
	#print("TITLE: ", title)
	event_data['title'] = title
	for tr in infobox_data:
		label = tr.next_element.next_element.string
		if label in ['Brand(s)', 'Date', 'City', 'Venue']:
			x = ""
			for c in label.next_element.children:
				if c.string == None:
					x += ", "
				else:
					x += c.string	
			#print(label, ": ", x)
			event_data[label] = x
	results = event_detail_soup.find('span', id='Results').parent.next_sibling.next_sibling

	index = 0
	#print(results.tbody.contents)
	for tr in results.tbody.find_all('tr'):
		if index > 0:
			competitors = []
			tds = tr.find_all('td')
			try:
				for a in tds[0].stripped_strings:
					competitors.append(a)
				stipulations = ', '.join([a.string for a in tds[1].find_all('a')])
				#print("COMPETITORS: ", competitors)
				#print("STIPULATIONS: ", stipulations)
				matches.append(
					{ "competitors": competitors,
					"stipulations": stipulations
					}
				)
			except:
				continue
			
			
		index += 1
	event_data['matches'] = matches

	#print(event_data)
	return event_data

def get_events(event):

	if len(event['class']) < 2:
		event = event.next_sibling.next_sibling		
	events_table = event.find('tbody')
	events_in_year = events_table.find_all('tr')

	return events_in_year

for year in range(1985,2024):
	event = soup.find('span', id=str(year)).parent.next_sibling.next_sibling
	try:
		events_in_year = get_events(event)

	except:	
		event = event.next_sibling.next_sibling
		events_in_year = get_events(event)

	print("AAAAA: ", events_in_year[1].find_all('td')[1].find('a')['href'])
	index = 0
	for tr in events_in_year:
		if index > 0:
			print("-----EVENT-----: ", tr)
			try:
				a = tr.find_all('td')[1].find('a')['href']
				print("THIS IS A---->>>>>: ", a)
				event_detail_list.append(get_event_detail(a))
			except:
				continue
		index += 1
		##print(year, " - ", a)
import json	
f = open("wwe_event_data.txt", "w")
json.dump(event_detail_list, f)

#print("******: ", event_list[0]['href'])
#next_page = requests.get(base_url + event_list[0]['href'])
#print(next_page)
#soup = BeautifulSoup(next_page.text, 'html.parser')
#print(soup.prettify())


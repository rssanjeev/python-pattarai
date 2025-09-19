import requests
import json
from pydantic import BaseModel 
from typing import List
from datetime import datetime

#POST_URL = "https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=d85a26a688732c7412f0ae18b01e"
#GET_URL = "https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=d85a26a688732c7412f0ae18b01e"

class Partner(BaseModel): 
  firstName: str
  lastName: str
  email: str
  country: str
  availableDates: List[str]


class Event():
  def __init__(self, attendeeCount, attendees, name, startDate):
    self.attendeeCount = attendeeCount
    self.attendees = attendees
    self.name: name
    self.startDate: startDate


def get_request() -> json: 
  response = requests.get(GET_URL)
  return json.loads(response.text)


def deserialize_json(text: json) -> List[Partner]:
  partners = []
  for item in text['partners']:
    partner = Partner(**item)
    partners.append(partner)
  return partners


def serialize_event(result) -> json:
  events = []
  for (country, item) in result.items():
    for date in item:
      events.append({
        'attendeeCount': len(item[date]),
        'attendees': item[date],
        'name': country,
        'startDate': date
      })
  return json.dumps({'countries': events})


def post_request(scheduled_events: json):
  post_req = requests.post(POST_URL, data = scheduled_events)
  return post_req.text


def get_formatted_date(date):
  return datetime.strptime(date, "%Y-%m-%d")


def get_date_with_max_partners(date_mapping):
  max_so_far = 0
  max_date = None
  for key, value in date_mapping.items():
    if len(value) > max_so_far:
      max_date = key
      max_so_far = len(value)

    if len(value) == max_so_far:
      if not max_date or max_date > key:
        max_date = key
  
  return max_date


def find_dates_for_country(country_partners):
  all_available_dates = sorted(list(set([date for p in country_partners for date in p.availableDates])))

  partners_available_on_date, results = {}, {}

  for date in all_available_dates:
    partners_available_on_date[date] = [p.email for p in country_partners if date in p.availableDates]

  for (d1, d2) in zip(all_available_dates[:-1], all_available_dates[1:]):
    diff = (get_formatted_date(d2) - get_formatted_date(d1)).days
    if not diff == 1:
      continue
    common_partners = list(set(partners_available_on_date[d1]) & set(partners_available_on_date[d2]))
    results[d1] = common_partners

  max_partners_date = get_date_with_max_partners(results)
  partners_for_max_date = results[max_partners_date] if max_partners_date else None
  return {max_partners_date: partners_for_max_date}


def find_dates(partners):
  country_partner_mapping = {}
  for p in partners:
    if p.country in country_partner_mapping:
      country_partner_mapping[p.country] += [p]
    else:
      country_partner_mapping[p.country] = [p]
  
  dates_for_country = {}
  for country in country_partner_mapping:
    dates_for_country[country] = find_dates_for_country(country_partner_mapping[country])

  return dates_for_country


def schedule_event(): 
  from pprint import pprint
  raw_output = get_request()
  partners = deserialize_json(raw_output)
  event_dates_per_country = find_dates(partners)
  pprint(event_dates_per_country)
  raw_events = serialize_event(event_dates_per_country)
  
  # pprint(raw_events)
  # response = post_request(raw_events)
  # print(response)

# calling the main function here
schedule_event()
import requests
import json

def fetch_police_events(location='Åre', events_limit=5):
    url = f"https://polisen.se/api/events?locationname={location}"
    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()[:events_limit]
        return events
    else:
        print("Failed to fetch data from Polisen API")
        return []

def print_events(events):
    for event in events:
        print(f"{event['name']}")
        #print(f"Datum/Tid: {event['datetime']}")
        print(f"Sammanfattning: {event['summary']}")
        #print(f"URL: https://polisen.se{event['url']}")
        #print(f"Typ: {event['type']}")
        #print(f"Plats: {event['location']['name']}"),
        #print(f"GPS: {event['location']['gps']}\n")

if __name__ == "__main__":
    events = fetch_police_events()
    if events:
        print_events(events)
    else:
        print("Inga händelser att visa.")
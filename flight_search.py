import datetime
import requests
from flight_data import FlightData

date = datetime.datetime.now()
d = date.strftime("%d")
m = date.strftime("%m")
date_list = []
for i in range(60):
    date1 = date + datetime.timedelta(days=i)
    date_list.append(date1.strftime("%d/%m/%Y"))


class FlightSearch:
    def __init__(self):
        self.tequila_endpoint = "https://tequila-api.kiwi.com"
        self.tequila_token = "fXomxrTHIRaO2CGfD3V-8ZPH65iVXELB"
        self.tequila_headers = {"apikey": self.tequila_token}

    def destination_code(self, city_name):
        query = {"term": city_name, "location_types": "city"}
        tequila_response = requests.get(f"{self.tequila_endpoint}/locations/query", headers=self.tequila_headers,
                                        params=query)
        results = tequila_response.json()["locations"]
        code = results[0]["code"]
        return code

    def search_flights(self, city_to: str, from_time: date, to_time: date, city_from):
        price_dict = {}
        price_list = []

        self.search_parms = {
            "fly_from": city_from,
            "fly_to": city_to,
            "date_to": to_time.strftime("%d/%m/%Y"),
            "date_from": from_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP",
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0
        }
        price_response = requests.get(url=f"{self.tequila_endpoint}/v2/search", headers=self.tequila_headers,
                                      params=self.search_parms)
        try:
            data = price_response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {city_to}")
            return None

        fligth_data = FlightData(
            price=data['price'],
            original_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"Fly to: {fligth_data.destination_city}, price: {fligth_data.price}")
        return fligth_data

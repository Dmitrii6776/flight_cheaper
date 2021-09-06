import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def destination_data(self):
        self.get_sheety_endpoint = "https://api.sheety.co/eb1e5ac575088944eeae58570d5b50db/flightCheaper/prices"
        self.sheety_data = requests.get(self.get_sheety_endpoint).json()
        return self.sheety_data["prices"]

    def update_destination_codes(self):
        put_sheety_endpoint = f"https://api.sheety.co/eb1e5ac575088944eeae58570d5b50db/flightCheaper/prices/"
        for row in self.sheety_data['prices']:
            sheety_body = {
                "price": {
                    'iataCode': row["iataCode"]
                }
            }
            result = requests.put(f"{put_sheety_endpoint}/{row['id']}", json=sheety_body)

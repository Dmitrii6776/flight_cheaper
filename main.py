import datetime

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.destination_data()
flight_search = FlightSearch()
notification = NotificationManager()

tomorow = datetime.datetime.now() + datetime.timedelta(days=1)
six_month_from_today = datetime.datetime.now() + datetime.timedelta(days=(30 * 6))
original_city_code = "LON"
if sheet_data[0]['iataCode'] == '':
    for row in sheet_data:
        row["iataCode"] = flight_search.destination_code(row['city'])

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

for row in sheet_data:
    flights = flight_search.search_flights(
        city_to=row["iataCode"],
        from_time=tomorow,
        to_time=six_month_from_today,
        city_from=original_city_code)
    if flights.price < row["lowestPrice"]:
        notification.send_mail(message=f"Price Alert. Only {flights.price}, "
                                       f"{flights.original_city}--{flights.destination_city} to fly from"
                                       f"{flights.origin_airport} to {flights.destination_airport}, from "
                                       f"{flights.out_date} to {flights.return_date}")





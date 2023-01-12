import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

url_base = "https://www.autoscout24.com/lst/skoda/octavia/ft_gasoline?fregfrom=2017&sort=standard&desc=0&cy=D&atype=C&ustate=N%2CU&fuel=B&powertype=kw&search_id=22qh7nyfpb9&page="


prices = []
registration_dates = []
odometer_values = []
fuel_consumption = []
for i in range(1, 16):
    url = url_base + str(i)
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    mileage = []
    km = bs.find_all("div", class_="VehicleDetailTable_container__mUUbY")
    for i in range(0, len(km)):
        mileage.append(km[i].get_text())
        car_info_list = km[i].get_text().split()
        registration_dates.append(car_info_list[1])
        fuel_consumption.append(car_info_list[6])
    odometer_values.extend([x.split(" ")[0] for x in mileage])
    names = bs.find_all("p", class_="Price_price__WZayw")
    for i in range(0, len(names)):
        prices.append(names[i].get_text())
    litres = []
    for s in fuel_consumption:
        if s != "previous":
            try:
                litres.append(float(re.search(r'\d+(\.\d+)?', s).group()))
            except AttributeError:
                continue

years = [code[5:9] for code in registration_dates]

smallest_list = len(litres)
prices = prices[:smallest_list]
odometer_values = odometer_values[:smallest_list]
years = years[:smallest_list]

money = [code[1:8] for code in prices]

my_data = {"price":money, "mileage": odometer_values, "fuel_per_100km":litres, "age": years}
my_df = pd.DataFrame(my_data)


my_df.to_csv('Skoda.csv', index=False)

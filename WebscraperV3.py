from ast import For
from glob import glob
from bs4 import BeautifulSoup
import requests
import re


def init():
    global car_make
    car_make = input(
        'What is the manufacturer of the car you want to check? \nPlease type it in as if it were a name (ex: type "Ford" not "ford" or "FORD" and "Austin Healey" not "Austin-Healey") ')
    global car_model
    car_model = input(
        'What is the model of the car you want to check? \nPlease type it in as if it were a name (ex: type "Mustang" not "mustang" or "MUSTANG" \nAdditionally, type numbers like (Porsche) "911" instead of nine eleven) ')
    global transmission_type
    transmission_type = input('Transmission Type: ')


def finding_listings():
    global run
    run = True
    while run:
        try:
            starting_mileage = int(input('What\'s the lowest mileage you want to find? ') or 0)
            ending_mileage = int(input('What\'s the highest mileage you want to find? ') or 999999)
            filtered_year_starting = int(input('What starting year would you like? ') or '1900')
            filtered_year_ending = int(input('What ending year would you like? ') or '2022')
            car_price_start = int(input('What starting price do you want? ') or 500)
            car_price_limit = int(input('What price do you want to end at? ') or 9999999999)
            run = False
        except ValueError:
            print('Invalid input. Reenter your mileage and years.')
            continue
    mileage_range = range(starting_mileage, ending_mileage)
    price_range = range(car_price_start, car_price_limit)
    listings = soup.find_all("li", class_='s-item s-item__pl-on-bottom s-item--watch-at-corner')
    year_range = range(filtered_year_starting, filtered_year_ending)
    if listings.count != 0:
        for listing in listings:
            for num in year_range:
                if str(num) in listing.span.text:  # this is the header-- if year is in listing header, continue
                    car_mileage_html = listing.find("span", class_='s-item__dynamic s-item__dynamicAttributes2')
                    car_mileage_plaintext = car_mileage_html.text
                    car_mileage_re1 = re.sub(r"Miles\: ", '', car_mileage_plaintext)
                    car_mileage_re2 = re.sub(r"\,", '', car_mileage_re1)
                    if int(car_mileage_re2) in mileage_range:
                        car_price_html = listing.find("span", class_='s-item__price')
                        car_price = car_price_html.text
                        car_name = listing.span.text
                        car_name_re = re.sub('New Listing', '', car_name)
                        car_price_re = re.sub(r'\$|\,', '', car_price)
                        car_price_float = float(car_price_re)
                        if int(car_price_float) in price_range:
                            print(car_name_re)
                            print(car_price_re)
                            print(f'Mileage: {car_mileage_re2}')
                        else:
                            continue


user_input = input('Do you want to search for a car? Type Quit for quit. ')


def main():
    init()
    if transmission_type.lower() == 'manual':
        url = requests.get(f'https://www.ebay.com/sch/i.html?_sacat=6001&makeval={car_make}&modelval={car_model}&LH_ItemCondition=3000%7C1000%7C2500&_nkw={car_make}+{car_model}&_fspt=1&_ipg=240&Transmission=Manual&_dcat=6236&LH_PrefLoc=99&_sop=3').text
        global soup
        soup = BeautifulSoup(url, "html.parser")
        finding_listings()
        return
    elif transmission_type.lower() == 'automatic':
            url = requests.get(f'https://www.ebay.com/sch/i.html?_sacat=6001&makeval={car_make}&modelval={car_model}&LH_ItemCondition=3000%7C1000%7C2500&_nkw={car_make}+{car_model}&_fspt=1&_ipg=240&Transmission=Automatic&_dcat=6236&LH_PrefLoc=99&_sop=3').text
            soup = BeautifulSoup(url, "html.parser")
            finding_listings()
            return
    else:
            url = requests.get(f'https://www.ebay.com/sch/i.html?_sacat=6001&makeval={car_make}&modelval={car_model}&LH_ItemCondition=3000%7C1000%7C2500&_nkw={car_make}+{car_model}&_fspt=1&_ipg=240&_dcat=6236&LH_PrefLoc=99&_sop=3').text
            soup = BeautifulSoup(url, "html.parser")
            finding_listings()
            return


while user_input.lower() != 'quit':
    main()
    user_input = input('Do you still want to search for cars? Type Quit to Quit. ')
else:
    print('Thank you for using the scraper. ')

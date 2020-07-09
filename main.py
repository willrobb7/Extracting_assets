import json
import logging
from pprint import pprint
import csv
from csv import writer
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)
domain = "infinityworkssandbox"
bamboo_api_key = "d69af137944291726d0b55e5fc3bb4a7e381bbe3"
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")

default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

def main():

    employees = get_employee_directory()
    data = []
    list_of_assets = []

    with open('myCsv.csv', 'w', newline='') as f: #Opens a CSV file with the headers of Serial Number and Asset Tag
        thewriter = csv.writer(f)

        thewriter.writerow(['Serial Number', 'Asset Tag'])


    for employee in employees:
        user_id = employee.get("id")
        assets = get_assets(user_id)

        if len(assets) == 1:
            inner_assets = assets[0]
            object_of_assets = inner_assets[0]


            for key in object_of_assets:
                if key == 'customSerial#1' or key == 'customAssetNumber':
                    data.append(object_of_assets[key])

            data_list = list(data)
            data.pop(0)
            data.pop(0)
            list_of_assets.append(data_list)
            print("Asset ready to be exported")
        else:
            print("No assets available")

        print("-"*20)

    # print(list_of_assets)
    for i in list_of_assets:
        print(i)
        append_list_as_row('myCsv.csv',i)

def append_list_as_row(file_name,to_add):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(to_add)


def get_employee_directory():
    response = requests.get(
        url=f"https://api.bamboohr.com/api/gateway.php/{domain}/v1/employees/directory",
        headers=default_headers,
        auth=bamboo_auth,
    )
    response.raise_for_status()
    return response.json().get("employees")



def get_assets(bamboo_id):
    response = requests.get(
        url=f"https://api.bamboohr.com/api/gateway.php/{domain}/v1/employees/{bamboo_id}/tables/customAssets1",
        headers=default_headers,

        params={"format": "JSON"},
        data=json.dumps({
            "title": "Asset Data Please",

            "fields": [
                "customAssets1"
            ]
        }),

        auth=bamboo_auth
    )
    response.raise_for_status()
    return response.json()






if __name__ == '__main__':
    main()


#TODO If more then one asset- check dictionary for laptop https://realpython.com/iterate-through-dictionary-python/ ref(pet in a_dict.keys())
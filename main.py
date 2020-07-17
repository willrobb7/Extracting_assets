import json
import logging
from pprint import pprint
import csv
from csv import writer
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)
domain = "infinityworks"
# bamboo_api_key = "" #Sandbox
bamboo_api_key = "" #Live
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")

default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

def main():

    employees = get_employee_directory()
    data = []
    list_of_assets = []
    is_laptop = []

    with open('myCsv.csv', 'w', newline='') as f: #Opens a CSV file with the headers of Serial Number and Asset Tag
        thewriter = csv.writer(f)

        thewriter.writerow(['Serial Number', 'Asset Tag'])


    for employee in employees:
        user_id = employee.get("id")
        assets = get_assets(user_id)

        if len(assets) > 0:
                inner_assets = assets[0]
                if len(inner_assets) > 0:
                    # print(inner_assets)

                    for asset in inner_assets:
                        # print(asset)
                        for key in asset:

                            if key == 'customAssetcategory1':
                                is_laptop.append(asset[key])
                                # print(is_laptop)
                                if is_laptop[0] != 'Laptop':
                                    print("Not Exporting asset, as it is not Laptop")
                                    is_laptop.pop(0)
                                    continue
                                else :
                                    for key in asset:
                                        if key == 'customSerial#1' or key == 'customAssetNumber':
                                            data.append(asset[key])
                                            # data_list = list(data)
                                            if len(is_laptop) > 0:
                                                is_laptop.pop(0)
                                        # print(data)
                                        if len(data) > 2:
                                            data.pop(0)
                                        if len(data) > 2:
                                            data.pop(0)
                                        if len(data) > 2:
                                            data.pop(0)
                                        # print(data)
                                        data_list = list(data)

                                    list_of_assets.append(data_list)
                                    # print (list_of_assets)
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
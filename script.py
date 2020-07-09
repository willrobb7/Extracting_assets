data = ["COZ2TWSVS87", "00812"]

with open('myCsv.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Serial Number', 'Asset Tag'])
    thewriter.writerow(data)

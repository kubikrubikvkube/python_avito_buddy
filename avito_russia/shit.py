import csv

if __name__ == '__main__':
    name_id = 0
    with open('names.csv', mode='w', newline='', encoding='utf-8') as names_file:
        reader = csv.reader(names_file)
        for name in reader:
            print(name)
        #writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        print("df")

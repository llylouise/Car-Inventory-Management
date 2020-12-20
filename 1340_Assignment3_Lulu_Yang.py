# Assignment #3
# INF1340 Section 1
# Fall-2017
# Lulu Yang

inventory = {}
records = []
file = open("a3.csv", "r")

def load_data(file, inventory, records):
    '''(file open for reading, dict of {str: list of str}, list}, list) -> None

       This function loads all the data from the input file into the dictionary(inventory) and the records list(records).
    '''
    for line in file:
        if not line.startswith('#'):
            accessory, model_number, year, colour, make, model,body_type, quantity = line.strip().split(',')
            if accessory not in inventory:
                inventory[accessory] = []
            inventory[accessory].append(model_number)
            records.append([model_number, year, colour, make, model, body_type, int(quantity)])
                      

def menu(inventory_size):
    '''(int) -> str

       This function displays the car inventory menu and reads the menu selection from the user, which is returned as a string. If the car inventory is empty, the function only displays menu options 1 and Quit. If the car inventory is not empty, the function displays the full menu.

       >>> menu(0):
           '1'
       >>> menu(2):
           '3'
    '''
    print('Car Inventory Menu')
    print('==================\n')
    print('1- Add a Car')
    if (inventory_size > 0):
        print('2- Remove a Car')
        print('3- Find a Car')
        print('4- Show Complete Inventory')
        print('5- Output Inventory to File')
    print('Q- Quit\n')
        
    selection = input('Enter your selection:')
    return selection

def find_index(records, model_number):
    '''(list, str) -> int

       This function searches the car records and returns the index of the car with a matching model number. The function returns -1 if the model number is not found.

       >>> find_index([[Backup Camera, NDAD7, 2017, Red, Mazda, MX-5, Sport, 3], [Heated Seats, EK13Z, 2003, Black, Chevy, Silverado, Truck, 7]], NDAD7)
           0
       >>> find_index([Heated Seats, EK13Z, 2003, Black, Chevy, Silverado, Truck, 7], [Fog Lights, KR32E, 2009, Orange, Toyota, Matrix, Wagon, 3], [Backup Camera, NDAD7, 2017, Red, Mazda, MX-5, Sport, 3], KR32E]
           1
    '''
    for i in range(len(records)):
        if records[i][0] == model_number:
            return i
    return -1

def add_car(inventory, records):
    '''(dict of {str: list of str}, list) -> None

       This function adds the key/value pair (accessory and model number) to the inventory and the car to the list of records iff the car is not already part of the inventory. If the car is already part of the inventory, the function asks the user the quantity to be added and increases the current quantity accordingly.
    '''
    model_number = input('\nEnter the model number:')
    index = find_index(records, model_number)
    if index == -1:
        accessory = input('Enter the car accessory:')
        year = input('Enter the year:')
        colour = input('Enter the colour:')
        make = input('Enter the make:')
        model = input('Enter the model:')
        body_type = input('Enter the body type:')
        quantity = int(input('Enter the quantity:'))
        if not accessory in inventory:
            inventory[accessory] = []
        inventory[accessory].append(model_number)        
        records.append([model_number, year, colour, make, model, body_type, quantity])            
        print('\nNew car successfully added\n\n')
    else:          
        print('\nCar already exists in inventory.')
        add_quantity = int(input('\nEnter the quantity to be added:'))
        records[index][6] += add_quantity
        print('Increased quantity by ', add_quantity, '. New quantity is: ', records[index][6], sep = '')
        print('\n')
 

def remove_car(inventory, records):
    '''(dict of {str:list of str}, list) -> None
       This function removes a car from the inventory and from the list of records iff the car quantity is one. If the car quantity is greater than one, it decreases the quantity by one. The function will also remove a key from the inventory iff the list of values is empty.
    '''
    accessory = input('\nEnter the accessory:')
    if accessory in inventory:
        model_number = input('Enter the model number:')
        if model_number in inventory[accessory]:
            index = find_index(records, model_number)
            if records[index][6] == 1:
                model_number_index = inventory[accessory].index(model_number)
                inventory[accessory].pop(model_number_index)
                records.pop(index)
                print('\nCar removed from inventory.\n\n')
            elif records[index][6] > 1:
                records[index][6] = records[index][6] - 1
                print('\Car quantity is greater than one.')
                print('Decreased quantity by 1. New quantity is: ', records[index][6], sep = '')
                print('\n')
            if inventory[accessory] == []:
                inventory.pop(accessory)
        else:
            print('No cars with model number ' + model_number + ' for accessory ' + accessory + '. Cannot remove car!\n\n')
    else:
        print('No cars for accessory ' + accessory + '. Cannot remove car!\n\n')


def find_car(inventory, records):
    '''(dict of {str: list of str}, list) -> None
       This function searches for a car model number for a given accessory. If the car is part of the inventory, the function prints the car data, tab-delimited on one line and the car accessory on the next line. If the accessory cannot be found in the inventory, the function prints the message: "'No car for accessory' + accessory + '.'". If the car cannot be found in the records, the function prints the message: "'No car with model number' + model_number + 'for accessory' + accessory + '.'" 
    '''
    accessory = input('\nEnter the accessory:')
    if accessory in inventory:
        model_number = input('Enter the model number:')
        if model_number in inventory[accessory]:
            index = find_index(records, model_number)
            print('\n')
            for data in records[index]:
                print(str(data) + '\t', end ='')
            print('\nAccessory:', accessory, '\n\n')
        else:
            print('No cars with model number ' + model_number + ' for accessory ' + accessory + '.\n\n')
    else:
        print('No cars for accessory ' + accessory + '.\n\n')

def show_inventory(inventory, records):
    '''(dict of {str: list of str}, list) -> None
       This function prints all the cars for every accessory, tab-delimited, one car per line.
    '''
    print('\nComplete Inventory:')
    print('==================\n')
    for accessory in inventory:
        print(accessory + ':')
        print('-' * len(accessory))
        model_number_list = inventory[accessory]
        for model_number in model_number_list:
            index = find_index(records, model_number)
            for data in records[index]:
                print(str(data) + '\t', end = '')
            print()
        print()
    print()

def output_inventory(file, inventory, records):
    '''(file open for writing, dict of {str: list of str}, list) -> None
       This function outpus all the cars for every accessory, tab-delimited, one car per line to the output file.
    '''
    file = open('output.txt', 'w')
    file.write('\nComplete Inventory:')
    file.write('\n==================\n\n')
    for accessory in inventory:
        file.write(accessory + ':\n')
        file.write('-' * len(accessory) + '\n')
        model_number_list = inventory[accessory]
        for model_number in model_number_list:
            index = find_index(records, model_number)       
            for data in records[index]:
                file.write(str(data) + '\t')
            file.write('\n')
        file.write('\n')
    file.write('\n\n')
    file.close()


load_data(file, inventory, records)
inventory_size = len(inventory)
selection = menu(inventory_size)

while selection != 'q' and selection != 'Q':
    if int(selection) == 1:
        add_car(inventory, records)
    elif len(inventory) == 0 or int(selection) <= 0 or int(selection) >= 6:
        print('Wrong selection, try again!\n\n')
    elif int(selection) == 2:
        remove_car(inventory, records)
    elif int(selection) == 3:
        find_car(inventory, records)
    elif int(selection) == 4:
        show_inventory(inventory, records)
    elif int(selection) == 5:
        output_inventory(file, inventory, records)
        print()
    inventory_size = len(inventory)
    selection = menu(inventory_size)
print('Goodbye!')  
        
                
        
    
    
    
    
    

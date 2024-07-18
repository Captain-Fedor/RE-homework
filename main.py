import re
from pprint import pprint
import csv

def read_file(file: str):
    with open(file, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    return contacts_list

def find_phone_number(data: list):
    phone_list = []
    text = ','.join(data)
    pattern = r'\+*[78]\s*\(*\d+\)*[\s-]*\d+[\s-]*\d+[\s-]*\d+\s*\(*[доб\.]*\s*\d*\)*'
    phone_numbers = re.findall(pattern, text)
    # phone_list.append(phone_number)
    '''str'''
    return phone_numbers

def format_phone_number(list):
    phone_formatted = []
    for number in list:
        pattern1 = r'(\+*[78])[\s-]*\(*(\d{3,5})\)*[\s-]*(\d+)[\s-]*(\d+)[\s-]*(\d+)\s*\(*[доб\.]*\s*(\d*)\)*'
        pattern2 = r'+7(\2)\3-\4-\5'
        phone = re.sub(pattern1, pattern2, number)
        find_ext = r'доб\.*\s*\d+'
        extension = re.findall(find_ext, number)
        # print(extension)
        if extension:
            find_ext_num = r'\d+'
            extension_number = ''.join(re.findall(find_ext_num, extension[0]))
            phone = f'{phone} доб.{extension_number}'
        phone_formatted.append(phone)

    return phone_formatted

def sort_name(data: list):
    name_sorted = []
    for l in range(3):
        name_split = data[l].split()
        for word in name_split:
            name_sorted.append(word)
    '''list'''
    return name_sorted

def same_name_search(name1, name2):
    ''' name1 имя в list_upload name2 имя для проверки'''
    if name1[0] == name2[0] and name1[1] == name2[1]:
        return True

def add_surname(name1, name2):
    ''' name1 имя в list_upload name2 имя для проверки'''
    if len(name1) == 2 and len(name2) == 3:
        name1.append(name2[2])
    return name1

def add_phone_number(phone_list1, phone_list2):
    '''добавление новых номеров то го же лица'''
    for phone in phone_list2:
        if phone not in phone_list1:
            phone_list1.append(phone)
    return phone_list1

def semifinal_list(data: list):
    data.pop(0)  # delete headline from csv file
    list_upload =[]
    for init_data in data:
        new_name = sort_name(init_data)
        formatted_phone = format_phone_number(find_phone_number(init_data))
        new_person = [new_name, formatted_phone]
        list_upload.append(new_person)
    return list_upload

def clear_duplicates(data: list):
    person_name1 = l[0][0]
    person_phone1 = l[0][1]
    no_duplicates = [[person_name1, person_phone1]]
    for item in data:
        match = 0
        for person in no_duplicates:
            if same_name_search(person[0], item[0]):
                person[0] = add_surname(person[0], item[0])
                person[1] = add_phone_number(person[1], item[1])
                match = 1
        if match == 0:
           no_duplicates.append(item)

    sorted_list =[]
    for item in no_duplicates:
        name = ' '.join([str(i) for i in item[0]])
        phone = ', '.join([str(i) for i in item[1]])
        sorted_list.append([name+' : '+phone])
    return sorted_list

def write_phonebook(data:list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=' ')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(data)


if __name__ == '__main__':

    contacts_list = read_file('phonebook_raw.csv')
    l = semifinal_list(contacts_list)
    result = clear_duplicates(semifinal_list(contacts_list))
    write_phonebook(result)



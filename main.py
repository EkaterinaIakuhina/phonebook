from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


result_contacts_list = [] 
result_contacts_list.append(contacts_list[0])


def clear_phone_format(phone):
  regex = r"(\+7|8)?\s*\(?(\d{1,3})\)?[-\s]*(\d{1,3})[-\s]*(\d{1,2})[-\s]*(\d{1,2})\s*\(?(доб.)?\s*(\d+)?\)?"
  clear_phone_with_adds = r"+7(\2)\3-\4-\5 \6\7"
  clear_phone_wo_adds = r"+7(\2)\3-\4-\5"

  if "доб." in phone:
    return re.sub(regex, clear_phone_with_adds, phone)
  else: 
    return re.sub(regex, clear_phone_wo_adds, phone)


new_contacts_list = {}
data_needed = ['organization', 'position', 'phone', 'email']

#добавляем в словарь по уникальному ФИ и подставляем к каждому свои данные
for contact in contacts_list[1:]:
    full_name = ' '.join(filter(lambda x: x != '', contact[:3]))
    full_name_list = full_name.split(' ')
    last_name, first_name = full_name_list[:2]
    person = f'{last_name} {first_name}'

    #создаем словарь для нового человека
    if person not in new_contacts_list.keys():
      new_contacts_list[person] = {'surname': '', 'organization': '', 'position': '', 'phone': '', 'email':''}

    #проверяем наличие отчества и добавляем, если не пусто
    if len(full_name_list) == 3: 
      surname = full_name_list[2]
      new_contacts_list[person]['surname'] = surname

    #добавляем остальные данные к нужному человеку, если не пусто
    rest_data = dict(zip(data_needed, contact[3:]))
    for key, value in rest_data.items():
       if value: 
          #приводим телефоны в порядок
          if key == 'phone':
            new_phone = clear_phone_format(value)
            new_contacts_list[person][key] = new_phone
          else:
            new_contacts_list[person][key] = value


for name_surname, rest_data_dict in new_contacts_list.items(): 
  contact_list = []
  last_name, first_name = name_surname.split(' ')
  contact_list.append(last_name)
  contact_list.append(first_name)
  for value in rest_data_dict.values():
    contact_list.append(value)
  
  result_contacts_list.append(contact_list)




# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(result_contacts_list)
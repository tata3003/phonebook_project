from pprint import pprint
import csv
import re
from collections import defaultdict

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Шаг 2: Выполнение обработки данных
def normalize_contacts(contacts):
    normalized_contacts = []
    phonebook = defaultdict(list)  # Используем defaultdict для хранения записей

    for contact in contacts[1:]:  # Пропускаем заголовок
        # Разделяем ФИО
        full_name = " ".join(contact[:3]).split()
        if len(full_name) == 2:  # Если указаны только ФИ
            lastname, firstname = full_name
            surname = ''
        elif len(full_name) == 3:  # Если указаны ФИО
            lastname, firstname, surname = full_name
        else:  # Если неверный формат
            continue

        # Нормализуем телефон
        phone = contact[5]
        phone = re.sub(r'\D', '', phone)  # Убираем все нечисловые символы
        if len(phone) == 10:  # Если это 10 цифр
            phone = f"+7({phone[:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:]}"
        elif len(phone) == 11 and phone.startswith('8'):  # Если это 11 цифр с 8
            phone = f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:]}"
        elif len(phone) == 11 and phone.startswith('7'):  # Если это 11 цифр с 7
            phone = f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:]}"

        # Добавляем контакт в телефонную книгу
        phonebook[(lastname, firstname)].append([lastname, firstname, surname, contact[3], contact[4], phone, contact[6]])

    # Объединяем дублирующиеся записи
    for key, records in phonebook.items():
        lastname, firstname = key
        surname = records[0][2]  # берем фамилию из первой записи
        organization = records[0][3]  # берем организацию из первой записи
        position = records[0][4]  # берем позицию из первой записи
        phone = records[0][5]  # берем телефон из первой записи
        email = records[0][6]  # берем email из первой записи
        # Если есть дубли, проверяем их и сохраняем только уникальные
        for record in records:
            if record[5] != phone:
                phone = record[5]  # Обновляем телефон, если он другой
            if record[6] and not email:
                email = record[6]  # Если email пустой, добавляем новый
        normalized_contacts.append([lastname, firstname, surname, organization, position, phone, email])

    return normalized_contacts

# Нормализуем контакты
contacts_list = normalize_contacts(contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)


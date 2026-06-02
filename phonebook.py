from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# pprint(contacts_list)

contacts_dict = {}

phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*"
    r"(\d{3})[\s-]*"
    r"(\d{2})[\s-]*"
    r"(\d{2})"
    r"(?:[\s]*(?:доб\.?|ext\.?)\s*(\d+))?"
)

for contact in contacts_list[1:]:
    lastname, firstname, surname = contact[0], contact[1], contact[2]
    organization, position, phone, email = contact[3], contact[4], contact[5], contact[6]

    fio = " ".join([lastname, firstname, surname]).split()
    lastname, firstname, surname = (fio + ["", "", ""])[:3]
    # pprint(fio)

    phone = phone_pattern.sub(
        lambda m: f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
                  + (f" доб.{m.group(6)}" if m.group(6) else ""),
        phone
    )

    key = (lastname, firstname)
    if key not in contacts_dict:
        contacts_dict[key] = [lastname, firstname, surname, organization, position, phone, email]
    else:
        old = contacts_dict[key]
        old[2] = old[2] or surname
        old[3] = old[3] or organization
        old[4] = old[4] or position
        old[5] = old[5] or phone
        old[6] = old[6] or email

contacts_list = [contacts_list[0]] + list(contacts_dict.values())
# pprint(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(contacts_list)
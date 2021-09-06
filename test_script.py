#!/usr/bin/env python3

import re
import sys
import csv
import operator

errors = {}
users = {}

with open('syslog.log', 'r') as file:
  for line in file.readlines():
    message = (re.search(r'(ERROR|INFO)',line)).group(1)
    user = (re.search(r'\(([\w\. ]*)\)', line)).group(1)
    match = re.search(r'ERROR (.*) ', line)
    if message == 'ERROR':
      if match is not None:
        e = match.group(1).replace('ERROR', '').strip()
        if e not in errors:
          errors[e] = 1
        else:
          errors[e] += 1

    if user not in users:
      users[user] = {}
      users[user]['INFO'] = 0
      users[user]['ERROR'] = 0
      if message == 'ERROR':
        users[user]['ERROR'] = 1
      else:
        users[user]['INFO'] = 1
    else:
      if message == 'ERROR':
        users[user]['ERROR'] += 1
      else:
        users[user]['INFO'] += 1
errors_list = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
errors_list.insert(0, ('Error', 'Count'))

users_list =sorted(users.items(), key=operator.itemgetter(0))
users_list.insert(0, ('Username', {'INFO', 'ERROR'}))

file.close()

with open('errors.csv', 'w') as f2:
  writer = csv.writer(f2)
  for key, value in errors_list:
    writer.writerow([key, value])
f2.close()
with open('users.csv', 'w') as f3:
  columns = ['Username', 'INFO', 'ERROR']
  writer = csv.DictWriter(f3, fieldnames = columns)
  writer.writeheader()
  writer = csv.writer(f3)
  for key, value in sorted(users.items()):
    writer.writerow([key, value['INFO'], value['ERROR']])
f3.close()
print(users_list)
print(errors_list)

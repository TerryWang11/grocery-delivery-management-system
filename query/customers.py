import logging
from sqlalchemy import text

QUERY_E = '''
SELECT 
    c.customer_id, 
    c.c_first_name,
    c.c_last_name,
    c.birth_date,
    c.phone,
    c.address,
    c.city,
    c.state,
    c.zip_code, 
    c.account_balance,
    m.start_date,
    m.end_date,
    m.points,
    m.level
FROM customers c 
LEFT OUTER JOIN member_customers m 
ON c.customer_id = m.customer_id
WHERE 0>1
'''

QUERY = '''
SELECT 
    c.customer_id, 
    c.c_first_name,
    c.c_last_name,
    c.birth_date,
    c.phone,
    c.address,
    c.city,
    c.state,
    c.zip_code, 
    c.account_balance,
    m.start_date,
    m.end_date,
    m.points,
    m.level
FROM customers c 
LEFT OUTER JOIN member_customers m 
ON c.customer_id = m.customer_id
WHERE 1>0
'''

queryMap = {
    'customer_id': " AND c.customer_id = '{}' ",
    'c_first_name': " AND c.c_first_name = '{}' ",
    'c_last_name': " AND c.c_last_name = '{}' ",
    'birth_date': " AND c.birth_date = '{}' ",
    'phone': " AND c.phone = '{}' ",
    'address': " AND c.address = '{}' ",
    'city': " AND c.city = '{}' ",
    'state': " AND c.state = '{}' ",
    'zip_code': " AND c.zip_code = '{}' ",
    'start_date': " AND m.start_date = '{}' ",
    'end_date': " AND m.end_date = '{}' ",
    'level': " AND m.level = '{}' "
}

def fetch(args):
    if (args['customer_id'] == '') & (args['c_first_name'] == '') & (args['c_last_name'] == '') \
        & (args['birth_date'] == '') & (args['phone'] == '') & (args['address'] == '') \
        & (args['city'] == '') & (args['state'] == '') & (args['zip_code'] == '')\
        & ('member_customers' not in args):
        #& (args['start_date'] == '') & (args['end_date'] == '' )& (args['level'] == ''):
        query = QUERY_E
    else: query = QUERY
    if args['customer_id'] != '': query += queryMap['customer_id'].format(args['customer_id'])
    if args['c_first_name'] != '': query += queryMap['c_first_name'].format(args['c_first_name'])
    if args['c_last_name'] != '': query += queryMap['c_last_name'].format(args['c_last_name'])
    if args['birth_date'] != '': query += queryMap['birth_date'].format(args['birth_date'])
    if args['phone'] != '': query += queryMap['phone'].format(args['phone'])
    if args['address'] != '': query += queryMap['address'].format(args['address'])
    if args['city'] != '': query += queryMap['city'].format(args['city'])
    if args['state'] != '': query += queryMap['state'].format(args['state'])
    if args['zip_code'] != '': query += queryMap['zip_code'].format(args['zip_code'])
    if 'member_customers' in args:
        if args['start_date'] != '': query += queryMap['start_date'].format(args['start_date'])
        if args['end_date'] != '': query += queryMap['end_date'].format(args['end_date'])
        if args['level'] != '': query += queryMap['level'].format(args['level'])
    query += 'ORDER BY c.customer_id'
    return query


UPDATE_C = '''
UPDATE customers SET
'''

UPDATE_M = '''
UPDATE member_customers SET
'''

updateMap = {
    'c_first_name': " c_first_name = '{}' ,",
    'c_last_name': " c_last_name = '{}' ,",
    'birth_date': " birth_date = '{}' ,",
    'phone': " phone = '{}' ,",
    'address': " address = '{}' ,",
    'city': " city = '{}' ,",
    'state': " state = '{}' ,",
    'zip_code': " zip_code = '{}' ,",
    'account_balance': " account_balance = '{}' ,",
    'start_date': " start_date = '{}' ,",
    'end_date': " end_date = '{}' ,",
    'points': " points = '{}' ,",
    'level': " level = '{}' ,",

    'customer_id': " WHERE customer_id = '{}'"
}

def update(args):
    query1 = UPDATE_C
    if args['c_first_name'] != '': query1 += updateMap['c_first_name'].format(args['c_first_name'])
    if args['c_last_name'] != '': query1 += updateMap['c_last_name'].format(args['c_last_name'])
    if args['birth_date'] != '': query1 += updateMap['birth_date'].format(args['birth_date'])
    if args['phone'] != '': query1 += updateMap['phone'].format(args['phone'])
    if args['address'] != '': query1 += updateMap['address'].format(args['address'])
    if args['city'] != '': query1 += updateMap['city'].format(args['city'])
    if args['state'] != '': query1 += updateMap['state'].format(args['state'])
    if args['zip_code'] != '': query1 += updateMap['zip_code'].format(args['zip_code'])
    if args['account_balance'] != '': query1 += updateMap['account_balance'].format(args['account_balance'])
    query1 = query1[0:-1]
    query1 += updateMap['customer_id'].format(args['customer_id'])
    if (args['c_first_name'] == '') & (args['c_last_name'] == '') \
        & (args['birth_date'] == '') & (args['phone'] == '') & (args['address'] == '') \
        & (args['city'] == '') & (args['state'] == '') & (args['zip_code'] == '')\
        & (args['account_balance'] == '') & ('member_customers' not in args):
        query1 = ''
    query2 = ''
    if 'member_customers' in args:
        query2 = UPDATE_M 
        if args['start_date'] != '': query2 += updateMap['start_date'].format(args['start_date'])
        if args['end_date'] != '': query2 += updateMap['end_date'].format(args['end_date'])
        if args['points'] != '': query2 += updateMap['points'].format(args['points'])
        if args['level'] != '': query2 += updateMap['level'].format(args['level'])
        query2 = query2[0:-1]
        query2 += updateMap['customer_id'].format(args['customer_id'])
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(query1)
    # print("xxxxxxxxxxxxxxxxxxx")
    # print(query2)
    # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    query = [query1,query2]
    return query

DELETE = '''
DELETE FROM customers
'''

def delete(args):
    if args['customer_id'] != '': 
        query = DELETE
        query += updateMap['customer_id'].format(args['customer_id'])
    else: query = ''
    return query

ADD_C = '''
INSERT INTO customers VALUES(
'''

ADD_M = '''
INSERT INTO member_customers (customer_id, start_date, end_date, points, level)
VALUES(
'''

def add(args):
    if (args['customer_id'] == '') or (args['phone'] == '') or (args['account_balance'] == ''):
        return ['','']
    query1 = ADD_C
    query1 += args['customer_id'] + ','
    if args['c_first_name'] != '': query1 += '\'' + args['c_first_name'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['c_last_name'] != '': query1 += '\'' + args['c_last_name'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['birth_date'] != '': query1 += '\'' +args['birth_date'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    query1 += '\'' + args['phone'] + '\'' + ','
    if args['address'] != '': query1 += '\'' + args['address'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['city'] != '': query1 += '\'' + args['city'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['state'] != '': query1 += '\'' + args['state'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['zip_code'] != '': query1 += '\'' + args['zip_code'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    query1 += args['account_balance'] + ')'
    query2 = ''
    if 'member_customers' in args:
        query2 = ADD_M
        query2 += args['customer_id'] + ','
        if args['start_date'] != '': query2 += '\'' + args['start_date'] + '\'' + ','
        else: query2 += 'DEFAULT,'
        if args['end_date'] != '': query2 += '\'' + args['end_date'] + '\'' + ','
        else: query2 += 'DEFAULT,'
        if args['points'] != '': query2 += args['points'] + ','
        else: query2 += 'DEFAULT,'
        query2 += '\''+args['level'] + '\'' + ')'
    query = [query1,query2]
    return query
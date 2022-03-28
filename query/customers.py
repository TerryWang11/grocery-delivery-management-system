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
    # print(args)
    # print(str(query))
    return query


UPDATE = '''
UPDATE customers 
'''

def update(args):
    query = []
    return query
MAX_DEL_ID = """
    SELECT MAX(delivery_man_id) FROM delivery_men
"""

QUERY = '''
SELECT 
    delivery_man_id, 
    d_first_name, 
    d_last_name,
    phone, 
    rating
FROM delivery_men
WHERE 1>0
'''

QUERY_E = '''
SELECT 
    delivery_man_id, 
    d_first_name, 
    d_last_name,
    phone, 
    rating
FROM delivery_men
WHERE 0>1
'''

queryMap = {
    'delivery_man_id': " AND delivery_man_id = '{}'",
    'd_first_name': " AND d_first_name = '{}'",
    'd_last_name': " AND d_last_name = '{}'",
    'phone': " AND phone = '{}'",
    'rating': " AND rating = '{}'"
}

def fetch(args):
    print(args)
    if (args['delivery_man_id'] == '') & (args['d_first_name'] == '') & (args['d_last_name'] == '') \
        & (args['phone'] == '') & (args['rating'] == ''):
        query = QUERY_E
    else: 
        query = QUERY
    if args['delivery_man_id'] != '': query += queryMap['delivery_man_id'].format(args['delivery_man_id'])
    if args['d_first_name'] != '': query += queryMap['d_first_name'].format(args['d_first_name'])
    if args['d_last_name'] != '': query += queryMap['d_last_name'].format(args['d_last_name'])
    if args['phone'] != '': query += queryMap['phone'].format(args['phone'])
    if args['rating'] != '': query += queryMap['rating'].format(args['rating'])
    query += 'ORDER BY delivery_man_id'
    return query

UPDATE = '''
UPDATE delivery_men SET
'''
updateMap = {
    'd_first_name': " d_first_name = '{}' ,",
    'd_last_name': " d_last_name = '{}' ,",
    'phone': " phone = '{}' ,",
    'rating': " rating = '{}' ,",

    'delivery_man_id': " WHERE delivery_man_id = '{}' "
}

def update(id, args):
    if int(args['delivery_man_id']) > id: return ''
    query = UPDATE
    if args['d_first_name'] != '': query += updateMap['d_first_name'].format(args['d_first_name'])
    if args['d_last_name'] != '': query += updateMap['d_last_name'].format(args['d_last_name'])
    if args['phone'] != '': query += updateMap['phone'].format(args['phone'])
    if args['rating'] != '': query += updateMap['rating'].format(args['rating'])
    query = query[0:-1]
    query += updateMap['delivery_man_id'].format(args['delivery_man_id'])
    if (args['d_first_name'] == '') & (args['d_last_name'] == '') \
        & (args['phone'] == '') & (args['rating'] == ''):
        query = ''
    return query


DELETE = '''
DELETE FROM delivery_men
'''

def delete(id, args):
    if int(args['delivery_man_id']) > id: return ''
    if args['delivery_man_id'] != '': 
        query = DELETE
        query += updateMap['delivery_man_id'].format(args['delivery_man_id'])
    else: query = ''
    return query

ADD = '''
INSERT INTO delivery_men VALUES(
'''

def add(id, args):
    if (args['phone'] == ''):
        return ''
    query = ADD
    query += str(id) + ','
    if args['d_first_name'] != '': query += '\'' + args['d_first_name'] + '\'' + ','
    else: query += 'DEFAULT,'
    if args['d_last_name'] != '': query += '\'' + args['d_last_name'] + '\'' + ','
    else: query += 'DEFAULT,'
    query += '\'' + args['phone'] + '\'' + ','
    if args['rating'] != '': query +=  args['rating'] + ')'
    else: query += 'DEFAULT' + ')'
    return query
MAX_PRO_ID = """
    SELECT MAX(product_id) FROM inventory
"""

QUERY = '''
SELECT
    product_id, 
    product_name, 
    product_type, 
    unit_price, 
    quantity_in_stock
FROM inventory
WHERE 1>0
'''

QUERY_E = '''
SELECT
    product_id, 
    product_name, 
    product_type, 
    unit_price, 
    quantity_in_stock
FROM inventory
WHERE 0>1
'''

queryMap = {
    'product_id': " AND product_id = '{}'",
    'product_name': " AND product_name = '{}'",
    'product_type': " AND product_type = '{}'",
    'unit_price': " AND unit_price = '{}'",
    'quantity_in_stock': " AND quantity_in_stock = '{}'"
}

def if_id_is_a_num(args):
    if args['product_id'].isdecimal(): return 1
    else: return 0

def fetch(args):
    if if_id_is_a_num(args) == 0: return ''
    if (args['product_id'] == '') & (args['product_name'] == '') & (args['product_type'] == '') \
        & (args['unit_price'] == '') & (args['quantity_in_stock'] == ''):
        query = QUERY_E
    else: 
        query = QUERY
    if args['product_id'] != '': query += queryMap['product_id'].format(args['product_id'])
    if args['product_name'] != '': query += queryMap['product_name'].format(args['product_name'])
    if args['product_type'] != '': query += queryMap['product_type'].format(args['product_type'])
    if args['unit_price'] != '': query += queryMap['unit_price'].format(args['unit_price'])
    if args['quantity_in_stock'] != '': query += queryMap['quantity_in_stock'].format(args['quantity_in_stock'])
    query += 'ORDER BY product_id'
    return query

UPDATE = '''
UPDATE inventory SET
'''
updateMap = {
    'product_name': " product_name = '{}' ,",
    'product_type': " product_type = '{}' ,",
    'unit_price': " unit_price = '{}' ,",
    'quantity_in_stock': " quantity_in_stock = '{}' ,",

    'product_id': " WHERE product_id = '{}' "
}

def update(id, args):
    if if_id_is_a_num(args) == 0: return ''
    if args['product_id'] == '' or int(args['product_id']) > id: return ''
    query = UPDATE
    if args['product_name'] != '': query += updateMap['product_name'].format(args['product_name'])
    if args['product_type'] != '': query += updateMap['product_type'].format(args['product_type'])
    if args['unit_price'] != '': query += updateMap['unit_price'].format(args['unit_price'])
    if args['quantity_in_stock'] != '': query += updateMap['quantity_in_stock'].format(args['quantity_in_stock'])
    query = query[0:-1]
    query += updateMap['product_id'].format(args['product_id'])
    if (args['product_name'] == '') & (args['product_type'] == '') \
        & (args['unit_price'] == '') & (args['quantity_in_stock'] == ''):
        query = ''
    return query

DELETE = '''
DELETE FROM inventory
'''
def delete(id, args):
    if if_id_is_a_num(args) == 0: return ''
    if int(args['product_id']) > id: return ''
    if args['product_id'] != '': 
        query = DELETE
        query += updateMap['product_id'].format(args['product_id'])
    else: query = ''
    return query

ADD = '''
INSERT INTO inventory (product_id, product_name, product_type, unit_price, quantity_in_stock)
VALUES(
'''

def add(id, args):
    query = ADD
    query += str(id) + ','
    if args['product_name'] != '': query += '\'' + args['product_name'] + '\'' + ','
    else: query += 'DEFAULT,'
    if args['product_type'] != '': query += '\'' + args['product_type'] + '\'' + ','
    else: query += 'DEFAULT,'
    if args['unit_price'] != '': query += args['unit_price'] + ','
    else: query += 'DEFAULT,'
    if args['quantity_in_stock'] != '': query += args['quantity_in_stock'] + ')'
    else: query += 'DEFAULT)'
    return query
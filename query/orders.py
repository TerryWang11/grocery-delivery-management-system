MAX_ORDER_ID = """
    SELECT MAX(order_id) FROM orders_place
"""

QUERY_E = '''
SELECT 
    o.order_id, 
    o.customer_id, 
    o.delivery_man_id,
    o.total_price, 
    o.order_status, 
    o.placed_date, 
    od.delivered_date,
    coi.product_id,
    i.product_name,
    coi.quantity
FROM 
((orders_place o LEFT OUTER JOIN orders_deliver od
ON o.order_id = od.order_id)
LEFT OUTER JOIN contain_order_items coi
ON o.order_id = coi.order_id)
LEFT OUTER JOIN inventory i
ON coi.product_id = i.product_id
WHERE 0>1
'''

QUERY = '''
SELECT 
    o.order_id, 
    o.customer_id, 
    o.delivery_man_id,
    o.total_price, 
    o.order_status, 
    o.placed_date, 
    od.delivered_date,
    coi.product_id,
    i.product_name,
    coi.quantity
FROM 
((orders_place o LEFT OUTER JOIN orders_deliver od
ON o.order_id = od.order_id)
LEFT OUTER JOIN contain_order_items coi
ON o.order_id = coi.order_id)
LEFT OUTER JOIN inventory i
ON coi.product_id = i.product_id
WHERE 1>0
'''

queryMap = {
    'order_id': "AND o.order_id = {} ",
    'customer_id': "AND o.customer_id = {} ",
    'delivery_man_id': "AND o.delivery_man_id = {} ",
    'total_price': "AND o.total_price = {} ",
    'order_status': "AND o.order_status = '{}' ",
    'placed_date': "AND o.placed_date = '{}' ",
    'delivered_date': "AND od.delivered_date = '{}' "
}

def if_id_is_a_num(args):
    if args['order_id'].isdecimal() or args['order_id'] == '': return 1
    else: return 0

def fetch(args):
    if if_id_is_a_num(args) == 0: return ''
    if (args['order_id'] == '') & (args['customer_id'] == '') & (args['delivery_man_id'] == '') \
        & (args['order_status'] == '') & (args['placed_date'] == '') \
        & (args['delivered_date'] == ''):
        query = QUERY_E
    else: query = QUERY
    if args['order_id'] != '': query += queryMap['order_id'].format(args['order_id'])
    if args['customer_id'] != '': query += queryMap['customer_id'].format(args['customer_id'])
    if args['delivery_man_id'] != '': query += queryMap['delivery_man_id'].format(args['delivery_man_id'])
    if args['order_status'] != '': query += queryMap['order_status'].format(args['order_status'])
    if args['placed_date'] != '': query += queryMap['placed_date'].format(args['placed_date'])
    query += 'ORDER BY o.order_id'
    return query

UPDATE_O = '''
UPDATE orders_place SET
'''
UPDATE_COI = '''
UPDATE contain_order_items SET
'''
UPDATE_OIF = '''
UPDATE order_items_from SET
'''
UPDATE_OD = '''
UPDATE orders_deliver SET
'''

updateMap = {
    'customer_id': " customer_id = {} ,",
    'delivery_man_id': " delivery_man_id = {} ,",
    'total_price': " total_price = {} ,",
    'order_status': " order_status = '{}' ,",
    'placed_date': " placed_date = '{}' ,",
    'delivered_date': " delivered_date = '{}' ,", 
    'product_id': "product_id = {} ,",
    'quantity': "quantity = {} ,",

    'order_id': " WHERE order_id = {} "
}

def update(id, args):
    if if_id_is_a_num(args) == 0: return ['','']
    if args['order_id'] == '' or int(args['order_id']) > id: return ['','']
    # update orders_place
    query1 = UPDATE_O
    if args['customer_id'] != '': query1 += updateMap['customer_id'].format(args['customer_id'])
    if args['delivery_man_id'] != '': query1 += updateMap['delivery_man_id'].format(args['delivery_man_id'])
    # if args['total_price'] != '': query1 += updateMap['total_price'].format(args['total_price'])
    if args['order_status'] != '': query1 += updateMap['order_status'].format(args['order_status'])
    if args['placed_date'] != '': query1 += updateMap['placed_date'].format(args['placed_date'])
    query1 = query1[0:-1]
    query1 += updateMap['order_id'].format(args['order_id'])
    if (args['customer_id'] == '') & (args['delivery_man_id'] == '') \
        & (args['order_status'] == '') \
        & (args['placed_date'] == '') & (args['delivered_date'] == ''):
        query1 = ''
    # update contain_order_items
    # query2 = UPDATE_COI
    # if args['product_id'] != '': query2 += updateMap['product_id'].format(args['product_id'])
    # if args['quantity'] != '': query2 += updateMap['quantity'].format(args['quantity'])
    # if (args['product_id'] == '') & (args['quantity'] == ''):
    #     query2 = ''
    # query2 = query2[0:-1]
    # query2 += updateMap['order_id'].format(args['order_id'])
    # update order_items_from
    # query3 = UPDATE_OIF
    # if args['product_id'] != '': query3 += updateMap['product_id'].format(args['product_id'])
    # else: query3 = ''
    # query3 = query3[0:-1]
    # query3 += updateMap['order_id'].format(args['order_id'])
    # update orders_deliver
    query4 = UPDATE_OD
    if args['delivery_man_id'] != '': query4 += updateMap['delivery_man_id'].format(args['delivery_man_id'])
    if args['customer_id'] != '': query4 += updateMap['customer_id'].format(args['customer_id'])
    # if args['total_price'] != '': query4 += updateMap['total_price'].format(args['total_price'])
    if args['order_status'] != '': query4 += updateMap['order_status'].format(args['order_status'])
    if args['delivered_date'] != '': query4 += updateMap['delivered_date'].format(args['delivered_date'])
    query4 = query4[0:-1]
    query4 += updateMap['order_id'].format(args['order_id'])
    if (args['customer_id'] == '') & (args['delivery_man_id'] == '') \
        & (args['order_status'] == '') & (args['delivered_date'] == ''):
        query4 = ''

    query = [query1, query4]
    print("query1:", query1)
    print("query4:", query4)
    return query


DELETE_O = '''
DELETE FROM orders_place
'''
DELETE_COI = '''
DELETE FROM contain_order_items
'''
DELETE_OIF = '''
DELETE FROM order_items_from
'''
DELETE_OD = '''
DELETE FROM orders_deliver
'''

def delete(id, args):
    if if_id_is_a_num(args) == 0: return ''
    if args['order_id'] == '' or int(args['order_id']) > id: return ''
    if args['order_id'] != '': 
        query1 = DELETE_O
        query1 += updateMap['order_id'].format(args['order_id'])
        query2 = DELETE_COI
        query2 += updateMap['order_id'].format(args['order_id'])
        query3 = DELETE_OIF
        query3 += updateMap['order_id'].format(args['order_id'])
        query4 = DELETE_OD
        query4 += updateMap['order_id'].format(args['order_id'])

        query = [query1, query2, query3, query4]
    else: query = ''
    return query


ADD_O = '''
INSERT INTO orders_place VALUES(
'''
ADD_COI = '''
INSERT INTO contain_order_items VALUES(
'''
ADD_OIF = '''
INSERT INTO order_items_from VALUES(
'''
ADD_OD = '''
INSERT INTO orders_deliver VALUES(
'''

def add(id, args):
    if (args['customer_id'] == '' or args['product_id'] == ''):
        return ''
    # add to orders_place
    query1 = ADD_O
    query1 += str(id) + ','
    query1 += '\'' + args['customer_id'] + '\'' + ','
    if args['total_price'] != '': query1 += '\'' + args['total_price'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['order_status'] != '': query1 += '\'' + args['order_status'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['delivery_man_id'] != '': query1 += '\'' + args['delivery_man_id'] + '\'' + ','
    else: query1 += 'DEFAULT,'
    if args['placed_date'] != '': query1 += '\'' + args['placed_date'] + '\'' + ')'
    else: query1 += 'DEFAULT' + ')'
    # add to contain_order_items
    query2 = ADD_COI
    query2 += str(id) + ','
    query2 += '\'' + args['product_id'] + '\'' + ','
    if args['quantity'] != '': query2 += '\'' + args['quantity'] + '\'' + ')'
    else: query2 += 'DEFAULT' + ')'
    # add to order_items_from
    query3 = ADD_OIF
    query3 += str(id) + ','
    query3 += '\'' + args['product_id'] + '\'' + ')'
    # add to orders_deliver
    query4 = ADD_OD
    query4 += str(id) + ','
    if args['delivery_man_id'] != '': query4 += '\'' + args['delivery_man_id'] + '\'' + ','
    else: query4 += 'DEFAULT,'
    if args['customer_id'] != '': query4 += '\'' + args['customer_id'] + '\'' + ','
    else: query4 += 'DEFAULT,'
    if args['total_price'] != '': query4 += '\'' + args['total_price'] + '\'' + ','
    else: query4 += 'DEFAULT,'
    if args['order_status'] != '': query4 += '\'' + args['order_status'] + '\'' + ','
    else: query4 += 'DEFAULT,'
    if args['delivered_date'] != '': query4 += '\'' + args['delivered_date'] + '\'' + ')'
    else: query4 += 'DEFAULT' + ')'
    query = [query1, query2, query3, query4]

    return query
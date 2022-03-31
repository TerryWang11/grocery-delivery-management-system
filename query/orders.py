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
    od.delivered_date
FROM orders_place o
LEFT OUTER JOIN orders_deliver od
ON o.order_id = od.order_id
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
    coi.product_id
FROM 
(orders_place o LEFT OUTER JOIN orders_deliver od
ON o.order_id = od.order_id)
LEFT OUTER JOIN contain_order_items coi
ON o.order_id = coi.order_id
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

def fetch(args):
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

updateMap = {
    'customer_id': " customer_id = {} ,",
    'delivery_man_id': " delivery_man_id = {} ,",
    'total_price': " total_price = {} ,",
    'order_status': " order_status = '{}' ,",
    'placed_date': " placed_date = '{}' ,",
    'delivered_date': " delivered_date = '{}' ,", 

    'order_id': " WHERE order_id = {} "
}

def update(id, args):
    if int(args['order_id']) > id: return ''
    query = UPDATE_O
    if args['customer_id'] != '': query += updateMap['customer_id'].format(args['customer_id'])
    if args['delivery_man_id'] != '': query += updateMap['delivery_man_id'].format(args['delivery_man_id'])
    if args['total_price'] != '': query += updateMap['total_price'].format(args['total_price'])
    if args['order_status'] != '': query += updateMap['order_status'].format(args['order_status'])
    if args['placed_date'] != '': query += updateMap['placed_date'].format(args['placed_date'])
    if args['delivered_date'] != '': query += updateMap['delivered_date'].format(args['delivered_date'])
    query = query[0:-1]
    query += updateMap['order_id'].format(args['order_id'])
    if (args['customer_id'] == '') & (args['delivery_man_id'] == '') \
        & (args['total_price'] == '') & (args['order_status'] == '') \
        & (args['placed_date'] == '') & (args['delivered_date'] == ''):
        query = ''
    return query
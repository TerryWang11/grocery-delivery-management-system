#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

import query.customers, query.orders, query.deliverymen, query.products
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
# DATABASEURI = "postgresql://user:password@104.196.152.219/proj1part2"
DATABASEURI = "postgresql://yw3536:22723536@35.211.155.104/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print (request.args)
  # return render_template("login.html")
  return render_template("home.html")



# Link to feature page
@app.route("/home/")
def home():
  return render_template("home.html")

@app.route("/customers/")
def customers():
  return render_template("customers.html")

@app.route("/deliverymen/")
def deliverymen():
  return render_template("deliverymen.html")

@app.route("/orders/")
def orders():
  return render_template("orders.html")

@app.route("/products/")
def products():
  return render_template("products.html")

# Implement specific query functions
# customers management
@app.route("/view_customers/",methods=['POST'])
def view_customers():
  cursor = g.conn.execute('''
  SELECT c.customer_id, c.c_first_name, c.c_last_name, c.phone,
  c.birth_date, c.address, c.city, c.state, c.zip_code, 
  c.account_balance, m.start_date, m.end_date, m.points, m.level
  FROM customers c 
  LEFT OUTER JOIN member_customers m 
  ON c.customer_id = m.customer_id
  ORDER BY c.customer_id;
''')
  result = []
  for c in cursor:
    result.append(c)
  return render_template("customers.html", **dict(data1 = result))

@app.route("/search_customers/",methods=['POST'])
def search_customers():
  q = query.customers.fetch(request.form)
  cursor = g.conn.execute(q)
  result = []
  for c in cursor:
    result.append(c)
  if(result == []): 
    result = 'There are no matching results.'
    return render_template("customers.html", **dict(data2_1 = result))
  else: 
    return render_template("customers.html", **dict(data2_2 = result))

@app.route("/update_customers/",methods=['POST'])
def update_customers():
  q1 = query.customers.MAX_CUS_ID
  cursor = g.conn.execute(q1)
  c_id = 0
  for c in cursor:
      c_id = c
  q = query.customers.update(c_id[0],request.form)
  if q[0] == '' and q[1] == '':
    result = 'Update failed. Please enter the correct customer_id and fill in at least one other field.'
  elif q[0] != '':
    g.conn.execute(q[0])
    if q[1] != '':
      g.conn.execute(q[1])
    result = 'Update successfully!'
  return render_template("customers.html", data3 = result)

@app.route("/delete_customers/",methods=['POST'])
def delete_customers():
  q1 = query.customers.MAX_CUS_ID
  cursor = g.conn.execute(q1)
  c_id = 0
  for c in cursor:
      c_id = c
  q = query.customers.delete(c_id[0],request.form)
  if q == '':
    result = 'Delete failed. Please enter the correct customer_id.'
  else: 
    g.conn.execute(q)
    result = "Delete successfully!"
  return render_template("customers.html", data4 = result)

@app.route("/add_customers/",methods=['POST'])
def add_customers():
  q1 = query.customers.MAX_CUS_ID
  cursor = g.conn.execute(q1)
  c_id = 0
  for c in cursor:
      c_id = c
  q = query.customers.add(c_id[0]+1, request.form)
  if q[0] == '':
    result = 'Create failed. Please fill in all fields marked with *.'
  else:
    g.conn.execute(q[0])
    if q[1] != '':
      g.conn.execute(q[1])
    result = 'Create successfully!'
  return render_template("customers.html", data5 = result)

# delivery men management
@app.route("/view_deliverymen/",methods=['POST'])
def view_deliverymen():
  cursor = g.conn.execute('''
  SELECT delivery_man_id, d_first_name, d_last_name,phone, rating
  FROM delivery_men
  ORDER BY delivery_man_id;
  ''')
  result = []
  for c in cursor:
    result.append(c)
  return render_template("deliverymen.html", **dict(data1 = result))

@app.route("/search_deliverymen/",methods=['POST'])
def search_deliverymen():
  q = query.deliverymen.fetch(request.form)
  cursor = g.conn.execute(q)
  result = []
  for c in cursor:
    result.append(c)
  print(result)
  if(result == []): 
    result = 'There are no matching results.'
    return render_template("deliverymen.html", **dict(data2_1 = result))
  else: 
    return render_template("deliverymen.html", **dict(data2_2 = result))

@app.route("/update_deliverymen/",methods=['POST'])
def update_deliverymen():
  q1 = query.deliverymen.MAX_DEL_ID
  cursor = g.conn.execute(q1)
  d_id = 0
  for c in cursor:
      d_id = c
  q = query.deliverymen.update(d_id[0], request.form)
  if q == '':
    result = 'Update failed. Please enter the correct delivery_man_id and fill in at least one other field.'
  else: 
    g.conn.execute(q)
    result = 'Update successfully!'
  return render_template("deliverymen.html", data3 = result)

@app.route("/delete_deliverymen/",methods=['POST'])
def delete_deliverymen():
  q1 = query.deliverymen.MAX_DEL_ID
  cursor = g.conn.execute(q1)
  d_id = 0
  for c in cursor:
      d_id = c
  q = query.deliverymen.delete(d_id[0], request.form)
  if q == '':
    result = 'Delete failed. Please enter the correct delivery_man_id.'
  else: 
    g.conn.execute(q)
    result = "Delete successfully!"
  return render_template("deliverymen.html", data4 = result)

@app.route("/add_deliverymen/",methods=['POST'])
def add_deliverymen():
  q1 = query.deliverymen.MAX_DEL_ID
  cursor = g.conn.execute(q1)
  d_id = 0
  for c in cursor:
      d_id = c
  q = query.deliverymen.add(d_id[0]+1, request.form)
  if q == '':
    result = 'Create failed. Please fill in all fields marked with *.'
  else: 
    g.conn.execute(q)
    result = "Create successfully!"
  return render_template("deliverymen.html", data5 = result)

# products management
@app.route("/view_inventory/",methods=['POST'])
def view_inventory():
  cursor = g.conn.execute('''
  SELECT product_id, product_name, product_type, unit_price, quantity_in_stock
  FROM inventory
  ORDER BY product_id;
  ''')
  result = []
  for c in cursor:
    result.append(c)
  return render_template("products.html", **dict(data1 = result))

@app.route("/search_products/",methods=['POST'])
def search_products():
  q = query.products.fetch(request.form)
  cursor = g.conn.execute(q)
  result = []
  for c in cursor:
    result.append(c)
  print(result)
  if(result == []): 
    result = 'There are no matching results.'
    return render_template("products.html", **dict(data2_1 = result))
  else: 
    return render_template("products.html", **dict(data2_2 = result))

@app.route("/update_products/",methods=['POST'])
def update_products():
  q1 = query.products.MAX_PRO_ID
  cursor = g.conn.execute(q1)
  p_id = 0
  for c in cursor:
      p_id = c
  q = query.products.update(p_id[0], request.form)
  if q == '':
    result = 'Update failed. Please enter the correct product_id and fill in at least one other field.'
  else: 
    g.conn.execute(q)
    result = 'Update successfully!'
  return render_template("products.html", data3 = result)

@app.route("/delete_products/",methods=['POST'])
def delete_products():
  q1 = query.products.MAX_PRO_ID
  cursor = g.conn.execute(q1)
  p_id = 0
  for c in cursor:
      p_id = c
  q = query.products.delete(p_id[0], request.form)
  if q == '':
    result = 'Delete failed. Please enter the correct product_id.'
  else: 
    g.conn.execute(q)
    result = "Delete successfully!"
  return render_template("products.html", data4 = result)

@app.route("/add_products/",methods=['POST'])
def add_products():
  q1 = query.products.MAX_PRO_ID
  cursor = g.conn.execute(q1)
  p_id = 0
  for c in cursor:
      p_id = c
  q = query.products.add(p_id[0] + 1, request.form)
  if q == '':
    result = 'Create failed. Please fill in all fields marked with *.'
  else: 
    g.conn.execute(q)
    result = "Create successfully!"
  return render_template("products.html", data5 = result)


# orders management
@app.route("/view_orders/",methods=['POST'])
def view_orders():
  cursor = g.conn.execute('''
  SELECT o.order_id, o.customer_id, o.delivery_man_id,
  o.total_price, o.order_status, o.placed_date, od.delivered_date
  FROM orders_place o
  LEFT OUTER JOIN orders_deliver od
  ON o.order_id = od.order_id
  ORDER BY o.order_id;
  ''')
  result = []
  for c in cursor:
    result.append(c)
  return render_template("orders.html", **dict(data1 = result))

@app.route("/search_orders/",methods=['POST'])
def search_orders():
  q = query.orders.fetch(request.form)
  print(q)
  cursor = g.conn.execute(q)
  result = []
  for c in cursor:
    result.append(c)
  if(result == []): 
    result = 'There are no matching results.'
    return render_template("orders.html", **dict(data2_1 = result))
  else: 
    return render_template("orders.html", **dict(data2_2 = result))



# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login', methods = ['GET','POST'])
def login():
  userid = request.args.get("Account Number")
  pwd = request.args.get("Password")
  print('userid:', userid)
  print('pwd:', pwd)
  digit = int(userid[0])
  cursor = g.conn.execute("SELECT * FROM manager_mana where account_number = %s and password_ = %s", userid, pwd)
  s = cursor.fetchall()
  cursor.close()
  if len(s) != 0:
    return render_template("home.html", err = userid)
  else:
    print("invalid account number or passward!")
    return render_template("login_fail.html", err = userid)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

# COMS4111 Project 1
## Author:  Zhuoyu Feng(zf2272), Yukun Wang(yw3536)
## Database: yw3536
## URL: http://34.73.53.129:8111/
### Descripetions
We built a web application for grocery delivery management, which is designed to help managers better manage customer information, delivery men information, orders information, and products information. 

As we proposed in part1, we divided this system into four functional sections, namely customers management, deliverymen management, orders management, and products management. We have basically completed all the features in the proposal. In addition, we have also completed the function of viewing customer history orders and viewing the item information contained in the order. 

We did not choose to implement the manager registration function because we think this system only needs a few stable managers, as we already stored their information including the matched account number and password in our database. Hence, we don't really need to design this function to add more account number - password pairs into our database, since this is not the core part of the whole system.

### Two interesting webpages
#### 1. Customers management page:
This page enables the user to manage all the data regarding the customers, which contains the following five functions:

1. View All Customers' Info

   Click the 'view' button, it will fetch a couple of important columns in terms of the customer by calling 'SELECT...FROM...' SQL syntax and display it as a table.

2. Search Customer & Order History

   This function enables the manager to search certain customers' information and their order history. It is done by using the *SELECT...FROM...LEFT OUTER JOIN...ON...WHERE...* SQL syntax, columns with nonempty inputs will be added to the *WHERE...* conditions.

3. Update Customer

   This function enables the manager to modify and update a specific customer's information, achieved by calling *UPDATE ... SET* plus the updated data of some attributes, read from the input boxes.

4. Delete Customer

   The manager is able to delete a specific customer by inputting *customer_id*. Then *DELETE FROM ...* will be executed in all the tables containing *customer_id*.

5. Create Customer

   When an order is placed by a new customer, it needs to be added to our database, the manager can do this using this function. It is done by using the *INSERT INTO ... VALUES( ... )* SQL syntax.


I think the "Search Customer & Order History" function is very useful because it can help managers quickly find a customer's purchase history for checking or understanding the customer's shopping habits. 

#### 2. Orders manegement page
This page enables the user to manage all the data regarding the orders, which contains the following five functions:

1. View All Orders Info

   Click the 'view' button, it will fetch a couple of important columns in terms of order by calling 'SELECT...FROM...' SQL syntax and display it as a table.

2. Search Order

   Users can retrieve all orders that match the information they input in the input boxes. For example, one can find all the orders that were delivered by a specific delivery man on a specific day by simply inputting the *Delivery Man ID* as well as the *Delivered Date* in the boxes. It is done by using the *SELECT...FROM...LEFT OUTER JOIN...ON...WHERE...* SQL syntax, columns with nonempty inputs will be added to the *WHERE...* conditions.

3. Update Order

   This function enables the manager to modify and update a specific order's information, achieved by calling *UPDATE ... SET* plus the updated data of some attributes, read from the input boxes.

4. Delete Order

   The manager is able to delete a specific order by inputting *order_id*. Then *DELETE FROM ...* will be executed in all the tables containing *order_id*.

5. Create Order

   When a new order is placed by a customer, it needs to be added to our database, the manager can do this using this function. Since all attributes in this function cover four tables, it needs to execute *INSERT INTO ... VALUES( ... )* in all those tables with appropriate orders considering some foreign keys' constraints.



​	The design of this page is interesting for the following reasons:

1. Since orders' information is covered in four tables, there are many cross-table operations.
2. We considered several boundary conditions, for example, the input IDs should be non-empty since they are primary keys, and they should be integers. We add some friendly instructions with those invalid inputs, to help the user input the correct information, e.g., 'Add failed. Please enter the necessary customer_id and product_id'.
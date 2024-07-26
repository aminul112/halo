# Simple Trading System with Python Django

Please build a simple trading system as a pure REST API with the endpoints outlined below. We
want to allow authenticated users the ability to place orders to buy and sell stocks and track the
overall value of their investments. Stock model will have 3 fields, they are id, name, and price. 
Id is the primary key in the Stock model.

## Endpoints:
1. Create an endpoint to let users place trades. When an order is placed we need to record
the quantity of the stock the user wants to buy or sell.
2. Create a cron that parses a CSV from a preconfigured directory to place trades in bulk.
3. Create an endpoint to retrieve the total value invested in a single stock by a user. To
calculate this - we need to sum all the value of all orders placed by the user for a single
stock. Order value is calculated by multiplying quantity and stock price.

## What we will be considering:
1. Use Poetry for package management
2. Following best practices of python3 and PEP8
3. Following Django best practices
4. Use of the Django ORM
5. Good testing practices
6. Following good object oriented design principles
7. Extending the outlined functionality is encouraged but not at the cost of code quality
8. application of SOLID principles in the designs will be highly regarded
9. Stock Model will have an id, name, and price.
10. Use Pytest module to write test cases
11. Write test cases for views using Client
12. Show Trade and Stock modules in Django Admin



## Possible Future Works:
1. Probably Add Token Authentication of Django DRF?

## About requirements:
1. I think it is important to keep track of which user holds which stocks and 
also how many of those. But the requirements are not clear if we need to check valid quantity and
ownership of stocks before buying or selling. To do this, we will need another model called 'StockOwnership' having 3 fields 'user', 'stock', and 'quantity' where both 'user' and 'stock' are foreign key. And then we need to establish relationship between Trade, StockOwnership and Stock models before a buy or sell.
2. I think that "the total value invested" should be calculated by current holding quantity and price. Anyway, I have done according to the requirement.
3. For this project I could not see a necessary case to use SOLID principles. However, since Django uses MVT architecture, it is very extensible by design.
4. 
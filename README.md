# capstone

For my final project i have created a bank application where customers can have access to:
* Transfer their money
* Buy Airtime (as we do here in my country (Nigeria), and also
* Pay bills.

Those views (transfer, buy airtime and pay bills) have their separate files in the pages folder so that whenever any of them is needed it will just be called up.


Staff are selected at random when a new customer is registered and they are attached to customers as their account manager, so a staff might have more than one customers.

A staff or an account manager have access to:
* view all the transactions made by their customers,
* Call customer for any Emergency,
* Send mail to customer,
* View customer expenditures under some specified category.


Another main feature of this web application is that from the Expenditure Category: 
* Properties,
* Food,
* Investement,
* shelter and
* Mecsellaneous.


and  Naration that the customer will provide while making transactions most expecially when transferring money (but for Buying airtime and paying bills the Category and Narations will be automatically generated) and will be use to analyse the customer's account which show how many percentage of total income spent on each category, that is it can show the customer that he/she has spent 40% of his/her income on Investement and 30% on Food for example.


My project has satisfied all the requirements:
* My project is sufficiently distinct from other projects,
* I've utilize Django (with more than one model) as my backend and Javascript as my Frontend and
* It's mobile responsive.


## For testing 

* You can find other customers account number by going to to the django admin panel (/admin) then Accounts model.
* Login as a staff and it will automatically redirect you to the staff page instead of customer page.
* While registering the via the admin page use the username field for email but i've created a staff and some customer already:

### Superuser:
    username: admin
    password: 12345

### Staff:
    Email: staff@3nitybank.com
    password: MANAGER12345

### Customers:
    Email: paulinnocent@email.com
    password: 12345
    Account Number: 2392146465
    Transaction Pin: 1234

    Email: foo@email.com
    password: 12345
    Account Number: 4678234741
    Transaction Pin: 1234
    
    Email: lilian@email.com
    password: 12345
    Account Number: 7112455646
    Transaction Pin: 1234
    

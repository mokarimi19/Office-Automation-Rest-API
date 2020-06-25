# Office-Automation-Rest-API
Django Rest Framework API for Office Automation (register user, register department, task management, ....)

This project cover followin tasks:
 - Add User as Employee (username, first name, last name, email)
 - Add Department by Admin User 
 - Request for Promotion from a regular employee to department employee
 - Request for Promotion from a  department employee to department manger
 - Create task for yourself and other department employee
 


# APIs

Most of APIs are represented on DRF API-Root Page Browsable API, **But not all of them**.

  "tasks":  "[http://127.0.0.1:8000/tasks/[pk]](http://127.0.0.1:8000/tasks/)"  
  
  "users": "http://127.0.0.1:8000/users/[pk]"(http://127.0.0.1:8000/users/)

  "department":  "[http://127.0.0.1:8000/department/[pk]](http://127.0.0.1:8000/department/)"
  
  "request":  "[http://127.0.0.1:8000/request/[pk]](http://127.0.0.1:8000/request/)"
  
  This is not apeared in API-Root Page, Because it is not register in router.
  
  "dashboard":  "[http://127.0.0.1:8000/dashboard/[pk]](http://127.0.0.1:8000/dashboard/)"
  
  
  # Functionalities
## Create Superuser
Default User of Django has been extented to meet requirements of project(Default process of creating new user in Django doesn't include first_name, last_name)

![](https://github.com/mokarimi19/Office-Automation-Rest-API/blob/cc303b1ebc395f8943fdffba1a468529837708ba/img/createsuperuser.PNG)

The custom user model is developed by extending AbstractUser model.

## Creating Users
List All user Just to All Visitors, But hey cann't Create New User.

Just UnAuthenticated User can create create.

  "users": "http://127.0.0.1:8000/users/[pk]"(http://127.0.0.1:8000/users/)


## Request Membership
Membership is request of regular employee who is not belong to any department to the admin or manager of the depatmen to become a member of that department.
  "request":  "[http://127.0.0.1:8000/request/[pk]](http://127.0.0.1:8000/request/)"
 
 Hint: It is recorded in database as "m"(initial of membership) to "request_type" field.
 
## Request Promotion
Promotion is a request of dapartment employee who wants to become of a department manger.
  "request":  "[http://127.0.0.1:8000/request/[pk]](http://127.0.0.1:8000/request/)"

 Hint: It is recorded in database as "e2m"(initial of "Employee to Manager") to "request_type" field.
 
 ## Dashboard
 All request will be listed to the user according to its rule:
 
 Unathenticated User will see nothing.
 
 Managers will see Membership request of regular employee to its department.
 
 Admin will see all type of reqests.
 
 They can access a request by its pk id. and reject or accept the request.
 
 rejected request will be removed from database table. accepted tabel will make change in database:
 
  - Make user manger of a department in case of acceptance of promotion request.
  - Make change to department name of user class in case of acceptance of membership request.
 
 ## Task manager
 All user can create task, an employee can just assign it to himsef, but manager assign it to himself or his department employee.
 
  "dashboard":  "[http://127.0.0.1:8000/dashboard/[pk]](http://127.0.0.1:8000/dashboard/)"


# Test
## POST Request Tools
Postman is the most popular API testing tools, I grab the headers and body from Inspect Element, Then I can Change the Parameters I need to test.

![](https://github.com/mokarimi19/Office-Automation-Rest-API/blob/master/img/postman.png)

There are also some more alternative method to test project in djando and DRF API, But definitely Postman API Testing Method is superior to all. The active way of testing API in this projec was Browsable API of DRF. All code has been written in a way than code be tested with  Browsable API of DRF


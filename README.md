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
  "users":  "[http://127.0.0.1:8000/users/[pk]](http://127.0.0.1:8000/users/)"
  "department":  "[http://127.0.0.1:8000/department/[pk]](http://127.0.0.1:8000/department/)"
  "request":  "[http://127.0.0.1:8000/request/[pk]](http://127.0.0.1:8000/request/)"
  This is not apeared in API-Root Page, Because it is not register in router.
  "dashboard":  "[http://127.0.0.1:8000/dashboard/[pk]](http://127.0.0.1:8000/dashboard/)"

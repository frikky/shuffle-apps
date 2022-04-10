# How to use MySQL App

## Authentication

For the authentication you will need:
- server;
- username;
- password;
- database.

> **Note:**
>
> If you want to use authentication to create databases only, leave the database field empty.
>
> You can set a dynamic value for the authentication fields by manually insert it. For example in the database field: **$exec.database**

## Actions

### Create Database
Create a new database. If you want you can also create one or more tables.
Fields:
- name;
- tables.

**Tables field example:**
Insert the table name and the query.
```
{
    "employees": "CREATE TABLE `employees` (`emp_no` int(11) NOT NULL AUTO_INCREMENT, `first_name` varchar(14) NOT NULL,  `last_name` varchar(16) NOT NULL,  PRIMARY KEY (`emp_no`)) ENGINE=InnoDB",
    "departments": "CREATE TABLE `departments` (`dept_no` char(4) NOT NULL, `dept_name` varchar(40) NOT NULL, PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)) ENGINE=InnoDB"
}
```

### Create Tables
Create one or more tables.
Fields:
- tables.

**Tables field example:**
Insert the table name and the query.
```
{
    "employees": "CREATE TABLE `employees` (`emp_no` int(11) NOT NULL AUTO_INCREMENT, `first_name` varchar(14) NOT NULL,  `last_name` varchar(16) NOT NULL,  PRIMARY KEY (`emp_no`)) ENGINE=InnoDB",
    "departments": "CREATE TABLE `departments` (`dept_no` char(4) NOT NULL, `dept_name` varchar(40) NOT NULL, PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)) ENGINE=InnoDB"
}
```

### Insert Data
Insert data into mysql table.

Fields:
- table;
- data.

**Data field example:**
MySQL field data in JSON format, *it can be a list or not*.
```
[{
    "title": "New Function1",
    "text": "testing",
    "time": 1617032159000
},
{
    "title": "New Function2",
    "text": "testing",
    "time": 1617032159000
}]
```

### Query Data
Query the data inside a table.

Fields:
- table;
- fields;
- condition.

**Fields example:**
Table fields to be return.
```
username, fname, lname, age
```

**Condition example:**
Query condition text after a WHERE clause.
```
age=23 and gender='M'
```

## Upcoming

- Improve the tables field to be needed just to insert the table name once in the json as key, and for the value the table fields syntax.
- Advanced Query - Allows the user to insert any type of query, as example with joins, etc...;

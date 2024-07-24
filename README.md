Mauritius Phone Numbers Generator
=================================

This will generate a list of Mauritius phone numbers. The phone numbers will be in the format 5xxxxxxx from the initial template provided by ICTA.

Requirements
------------

- Python 3
- SQLite3


Usage
-----

```sh
$ python3 main.py
```

Output
------

This will generate a `complete_numbers.db` which you can query to get the phone numbers.

```sh
$ sqlite3 complete_numbers.db
sqlite> SELECT * FROM numbers LIMIT 5;
```

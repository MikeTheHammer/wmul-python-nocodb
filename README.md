# NocoDB Python Client

NocoDB is a great Airtable alternative. This client allows python developers
to use NocoDB API in a simple way. This is a fork of https://github.com/elchicodepython/python-nocodb .

## Usage

### Client configuration
```python
from wmul-nocodb.nocodb import NocoDBProject, APIToken, JWTAuthToken
from wmul-nocodb.filters import LikeFilter, EqFilter, And
from wmul-nocodb.infra.requests_client import NocoDBRequestsClient


# Usage with API Token
client = NocoDBRequestsClient(
        # Your API Token retrieved from NocoDB conf
        APIToken("YOUR-API-TOKEN"),
        # Your nocodb root path
        "http://localhost:8080"
)

# Usage with JWT Token
client = NocoDBRequestsClient(
        # Your API Token retrieved from NocoDB conf
        JWTAuthToken("your.jwt.token"),
        # Your nocodb root path
        "http://localhost:8080"
)
```

### Project creation
```python
# Example with default database
project_body = {"title": "My new project"}

# Example with Postgresql
project_body = {
    "title": "MyProject",
    "bases": [
        {
            "type": "pg",
            "config": {
                "client": "pg",
                "connection": {
                    "host": "localhost",
                    "port": "5432",
                    "user": "postgres",
                    "password": "postgres",
                    "database": "postgres"
                },
                "searchPath": [
                    "public"
                ]
            },
            "inflection_column": "camelize",
            "inflection_table": "camelize"
        }
    ],
    "external": True
}

project = client.project_create(body=project_body)
```

### Project selection
```python
# Be very carefull with org, project_name and table names
# weird errors from nocodb can arrive if they are wrong
# example: id is not defined...
# probably they will fix that in a future release.
project = NocoDBProject(
        "noco", # org name. noco by default
        "myproject" # project name. Case sensitive!!
)

```

### Table rows operations
```python
table_name = "tablename"

# Retrieve a page of rows from a table
table_rows = client.table_row_list(project, table_name)

# Retrieve the first 1000 rows
table_rows = client.table_row_list(project, table_name, params={'limit': 1000})

# Skip 100 rows
table_rows = client.table_row_list(project, table_name, params={'offset': 100})
```

⚠️ Seems that we can't retrieve more than 1000 rows at the same time but we can paginate
 to retrieve all the rows from a table

Pagination example

```python

first_100_rows = client.table_row_list(project, table_name, params={'limit': 100})
next_100_rows = client.table_row_list(project, table_name, params={'limit': 100, 'offset': 100})
next_100_rows = client.table_row_list(project, table_name, params={'limit': 100, 'offset': 200})
```

More row operations

```python
# Filter the query
table_rows = client.table_row_list(project, table_name, LikeFilter("name", "%sam%"))
table_rows = client.table_row_list(project, table_name, And(LikeFilter("name", "%sam%"), EqFilter("age", 26)))
table_rows = client.table_row_list(project, table_name, filter_obj=EqFilter("Id", 100))

# Filter and count rows
count = client.table_count(project, table_name, filter_obj=EqFilter("Id", 100))

# Find one row
table_row = client.table_find_one(project, table_name, filter_obj=EqFilter("Id", 100), params={"sort": "-created_at"})

# Retrieve a single row
row_id = 10
row = client.table_row_detail(project, table_name, row_id)

# Create a new row
row_info = {
    "name": "my thoughts",
    "content": "i'm going to buy samuel a beer 🍻 because I 💚 this module",
    "mood": ":)"
}
client.table_row_create(project, table_name, row_info)

# Update a row
row_id = 2
row_info = {
    "content": "i'm going to buy samuel a new car 🚙 because I 💚 this module",
}
client.table_row_update(project, table_name, row_id, row_info)

# Delete a row (only if you've already bought me a beer)
client.table_row_delete(project, table_name, row_id)
```

### Available filters

- EqFilter
- EqualFilter (Alias of EqFilter)
- NotEqualFilter
- GreaterThanFilter
- GreaterOrEqualFilter
- LessThanFilter
- LessOrEqualFilter
- LikeFilter
- Or
- Not
- And

#### Combining filters using Logical operations

```python
from wmul-nocodb import filters

# Basic filters...
nick_filter = filters.EqFilter("nickname", "elchicodepython")
country_filter = filters.EqFilter("country", "es")
girlfriend_code = filters.EqFilter("gfcode", "404")
current_mood_code = filters.EqFilter("moodcode", "418")

# Combining filters using logical filters
or_filter = filters.Or(nick_filter, country_filter)
and_filter = filters.And(girlfriend_code, current_mood_code)

# Negating filters with a Not filter
not_me = filters.Not(filters.EqFilter("nickname", "elchicodepython"))

# You can also combine combinations
or_combined_filter = filters.Or(or_filter, and_filter)
and_combined_filter = filters.And(or_filter, and_filter)

```

### Using custom filters

Nocodb is evolving and new operators are coming with each release.

Most of the basic operations are inside this package but you could need some new
feature that could not be added yet.
For those filters you can build your own.

Example for basic filters:

```python
from wmul-nocodb.filters.factory import basic_filter_class_factory

BasicFilter = basic_filter_class_factory('=')
table_rows = client.table_row_list(project, table_name, BasicFilter('age', '16'))

```

You can find the updated list of all the available nocodb operators [here](https://docs.nocodb.com/developer-resources/rest-apis/#comparison-operators).

In some cases you might want to write your own filter string as described in the previous link.
For that cases you can use the less-semmantic RawFilter.

```python
from wmul-nocodb.filters.raw_filter import RawFilter

table_rows = client.table_row_list(project, table_name, RawFilter('(birthday,eq,exactDate,2023-06-01)'))
```

In some cases we might want to have a file with some custom raw filters already defined by us.
We can easily create custom raw filter classes using `raw_template_filter_class_factory`.

```python
from wmul-nocodb.filters.factory import raw_template_filter_class_factory

BirthdayDateFilter = raw_template_filter_class_factory('(birthday,eq,exactDate,{})')
ExactDateEqFilter = raw_template_filter_class_factory('({},eq,exactDate,{})')
ExactDateOpFilter = raw_template_filter_class_factory('({},{op},exactDate,{})')

table_rows = client.table_row_list(project, table_name, BirthdayDateFilter('2023-06-01'))
table_rows = client.table_row_list(project, table_name, ExactDateEqFilter('column', '2023-06-01'))
table_rows = client.table_row_list(project, table_name, ExactDateOpFilter('column', '2023-06-01', op='eq'))
```


Credits to @MitPitt for asking this feature.

## Author notes

This is a (maybe temporary?) fork of https://github.com/elchicodepython/python-nocodb


## Contributors


### To Original Project
![Contributors image](https://contrib.rocks/image?repo=elchicodepython/python-nocodb)


- Samuel López Saura @elchicodepython
- Ilya Sapunov @davert0
- Delena Malan @delenamalan
- Jan Scheiper @jangxx


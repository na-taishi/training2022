category_addition = '''
INSERT INTO category(
    name
)
VALUES(
    ?
)
'''

id_fetch = '''
SELECT
    category_id
FROM
    category
WHERE
    name = ?
'''

all_name_fetch = '''
SELECT
    name
FROM
    category
'''

all_fetch = '''
SELECT
    *
FROM
    category
'''
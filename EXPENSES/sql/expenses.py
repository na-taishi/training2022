daily_addition = '''
INSERT INTO expenses_daily(
    name ,
    payment,
    category_id,
    year,
    month,
    day
)
SELECT
    ?,
    ?,
    category_id,
    ?,
    ?,
    ?
FROM
    category
WHERE
    name = ?
'''

monthly_addition = '''
INSERT INTO expenses_monthly(
    name ,
    payment,
    category_id,
    year,
    month
)
SELECT
    ?,
    ?,
    category_id,
    ?,
    ?
FROM
    category
WHERE
    name = ?
'''

yearly_addition = '''
INSERT INTO expenses_yearly(
    name ,
    payment,
    category_id,
    year
)
SELECT
    ?,
    ?,
    category_id,
    ?
FROM
    category
WHERE
    name = ?
'''

daily_update = '''
UPDATE
    expenses_daily
SET
    name = ?,
    payment = ?,
    category_id = (
        SELECT
            category_id
        FROM
            category
        WHERE
            name = ?
    )
WHERE
    expenses_daily_id = ?
'''

monthly_update = '''
UPDATE
    expenses_monthly
SET
    name = ?,
    payment = ?,
    category_id = (
        SELECT
            category_id
        FROM
            category
        WHERE
            name = ?
    )
WHERE
    expenses_monthly_id = ?
'''

yearly_update = '''
UPDATE
    expenses_yearly
SET
    name = ?,
    payment = ?,
    category_id = (
        SELECT
            category_id
        FROM
            category
        WHERE
            name = ?
    )
WHERE
    expenses_yearly_id = ?
'''

daily_delete = '''
DELETE
FROM
    expenses_daily
WHERE
    expenses_daily_id = ?
'''

monthly_delete = '''
DELETE
FROM
    expenses_monthly
WHERE
    expenses_monthly_id = ?
'''

yearly_delete = '''
DELETE
FROM
    expenses_yearly
WHERE
    expenses_yearly_id = ?
'''

daily_fetch_to_front = '''
SELECT
    e.expenses_daily_id,
    e.name,
    e.payment,
    c.name
FROM
    expenses_daily AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
    AND e.month = ?
    AND e.day = ?
'''

monthly_fetch_to_front = '''
SELECT
    e.expenses_monthly_id,
    e.name,
    e.payment,
    c.name
FROM
    expenses_monthly AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
    AND e.month = ?
'''

yearly_fetch_to_front = '''
SELECT
    e.expenses_yearly_id,
    e.name,
    e.payment,
    c.name
FROM
    expenses_yearly AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
'''


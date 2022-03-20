daily_fetch_to_front = '''
SELECT
    c.name,
    SUM(e.payment)
FROM
    expenses_daily AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
    AND e.month = ?
    AND e.day = ?
GROUP BY
    c.name
'''

monthly_fetch_to_front = '''
SELECT
    c.name,
    SUM(e.payment)
FROM
    expenses_monthly AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
    AND e.month = ?
GROUP BY
    c.name
'''

yearly_fetch_to_front = '''
SELECT
    c.name,
    SUM(e.payment)
FROM
    expenses_yearly AS e
    INNER JOIN
        category AS c
    ON  e.category_id = c.category_id
WHERE
    e.year = ?
GROUP BY
    c.name
'''
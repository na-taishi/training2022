date_list_daily = '''
SELECT
    year,
    month,
    day
FROM
    expenses_daily
GROUP BY
    year,
    month,
    day
'''

date_list_monthly = '''
SELECT
    year,
    month
FROM
    expenses_monthly
GROUP BY
    year,
    month
'''

date_list_yearly = '''
SELECT
    year
FROM
    expenses_yearly
GROUP BY
    year
'''
category = '''
CREATE TABLE category(
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
'''

expenses_daily = '''
CREATE TABLE expenses_daily(
    expenses_daily_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    payment INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
)
'''

expenses_monthly = '''
CREATE TABLE expenses_monthly(
    expenses_monthly_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    payment INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL
)
'''

expenses_yearly = '''
CREATE TABLE expenses_yearly(
    expenses_yearly_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    payment INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    year INTEGER NOT NULL
)
'''
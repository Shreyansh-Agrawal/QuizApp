'''
    Queries for database operations
'''

class InitializationQueries:
    '''Contains queries for creation of db tables'''

    CREATE_USERS_TABLE = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            role TEXT,
            registration_date TEXT
        )'''

    CREATE_CREDENTIALS_TABLE= '''
        CREATE TABLE IF NOT EXISTS credentials (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            isPasswordChanged INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )'''

    CREATE_SCORES_TABLE = '''
        CREATE TABLE IF NOT EXISTS scores (
            score_id TEXT PRIMARY KEY,
            user_id TEXT,
            score INTEGER,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )'''

    CREATE_CATEGORIES_TABLE = '''
        CREATE TABLE IF NOT EXISTS categories (
            category_id TEXT PRIMARY KEY,
            category_name TEXT
        )'''

    CREATE_QUESTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS questions (
            question_id TEXT PRIMARY KEY,
            category_id TEXT,
            question_text TEXT,
            question_type TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE
        )'''

    CREATE_OPTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS options (
            option_id TEXT PRIMARY KEY,
            question_id TEXT,
            option_text TEXT,
            isCorrect INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE
        )'''


class Queries:
    '''Contains database queries'''

    INSERT_USER_DATA = 'INSERT INTO users VALUES (?, ?, ?, ?, ?)'
    INSERT_CREDENTIALS = 'INSERT INTO credentials VALUES (?, ?, ?, ?)'
    GET_USER_DATA = '''
        SELECT username, name, email, registration_date
        FROM users INNER JOIN credentials ON users.user_id = credentials.user_id
        where role = ?
        '''
    GET_CREDENTIALS = '''
        SELECT password, role, isPasswordChanged
        FROM credentials INNER JOIN users ON credentials.user_id = users.user_id 
        WHERE username = ?
        '''

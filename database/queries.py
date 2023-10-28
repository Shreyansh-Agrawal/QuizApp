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
            admin_id TEXT,
            admin_name TEXT,
            category_name TEXT UNIQUE,
            FOREIGN KEY (admin_id) REFERENCES users (user_id)
        )'''

    CREATE_QUESTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS questions (
            question_id TEXT PRIMARY KEY,
            category_id TEXT,
            admin_id TEXT,
            admin_name TEXT,
            question_text TEXT,
            question_type TEXT,
            FOREIGN KEY (admin_id) REFERENCES users (user_id),
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

    ENABLE_FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'


class Queries:
    '''Contains database queries'''

    INSERT_USER_DATA = 'INSERT INTO users VALUES (?, ?, ?, ?, ?)'

    INSERT_CREDENTIALS = 'INSERT INTO credentials VALUES (?, ?, ?, ?)'

    INSERT_OPTION = 'INSERT INTO options VALUES (?, ?, ?, ?)'

    INSERT_CATEGORY = 'INSERT INTO categories VALUES (?, ?, ?, ?)'

    INSERT_QUESTION = 'INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?)'

    GET_USER_BY_ROLE = '''
        SELECT username, name, email, registration_date
        FROM users INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE role = ?
    '''

    GET_USER_BY_USERNAME = '''
        SELECT username, name, email, registration_date
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = ?
    '''

    GET_ADMIN_ID_NAME_BY_USERNAME = '''
        SELECT users.user_id, name
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = ?
    '''

    GET_CREDENTIALS_BY_USERNAME = '''
        SELECT password, role, isPasswordChanged
        FROM credentials INNER JOIN users ON credentials.user_id = users.user_id 
        WHERE username = ?
    '''

    GET_ALL_CATEGORIES = 'SELECT category_name, admin_name FROM categories'
    GET_CATEGORY_ID_BY_NAME = 'SELECT category_id FROM categories WHERE category_name = ?'
    GET_ALL_QUESTIONS = '''
        SELECT category_name, question_text, question_type, questions.admin_name
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        ORDER BY category_name
    '''

    DELETE_USER_BY_EMAIL = 'DELETE FROM users WHERE email = ?'

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
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''

    CREATE_SCORES_TABLE = '''
        CREATE TABLE IF NOT EXISTS scores (
            score_id TEXT PRIMARY KEY,
            user_id TEXT,
            score INTEGER,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''

    CREATE_CATEGORIES_TABLE = '''
        CREATE TABLE IF NOT EXISTS categories (
            category_id TEXT PRIMARY KEY,
            admin_id TEXT,
            admin_username TEXT,
            category_name TEXT UNIQUE,
            FOREIGN KEY (admin_id) REFERENCES users (user_id)
        )'''

    CREATE_QUESTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS questions (
            question_id TEXT PRIMARY KEY,
            category_id TEXT,
            admin_id TEXT,
            admin_username TEXT,
            question_text TEXT,
            question_type TEXT,
            FOREIGN KEY (admin_id) REFERENCES users (user_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''

    CREATE_OPTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS options (
            option_id TEXT PRIMARY KEY,
            question_id TEXT,
            option_text TEXT,
            isCorrect INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''

    ENABLE_FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'


class Queries:
    '''Contains database queries'''

    INSERT_USER_DATA = 'INSERT INTO users VALUES (?, ?, ?, ?, ?)'

    INSERT_CREDENTIALS = 'INSERT INTO credentials VALUES (?, ?, ?, ?)'

    INSERT_OPTION = 'INSERT INTO options VALUES (?, ?, ?, ?)'

    INSERT_CATEGORY = 'INSERT INTO categories VALUES (?, ?, ?, ?)'

    INSERT_QUESTION = 'INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?)'

    INSERT_USER_QUIZ_SCORE = 'INSERT INTO scores VALUES (?, ?, ?, ?)'

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

    GET_USER_ID_BY_USERNAME = '''
        SELECT users.user_id
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = ?
    '''

    GET_CREDENTIALS_BY_USERNAME = '''
        SELECT password, role, isPasswordChanged
        FROM credentials INNER JOIN users ON credentials.user_id = users.user_id 
        WHERE username = ?
    '''

    GET_ALL_CATEGORIES = 'SELECT category_name, admin_username FROM categories'

    GET_CATEGORY_ID_BY_NAME = 'SELECT category_id FROM categories WHERE category_name = ?'

    GET_ALL_QUESTIONS_DETAIL = '''
        SELECT category_name, question_text, question_type, option_text, questions.admin_username
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1
        ORDER BY category_name
    '''

    GET_RANDOM_QUESTIONS_BY_CATEGORY = '''
        SELECT question_text, question_type, option_text
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1 AND category_name = ?
        ORDER BY RANDOM() LIMIT 10
    '''

    GET_LEADERBOARD = '''
        SELECT username, MAX(score), timestamp 
        FROM scores
        INNER JOIN credentials ON scores.user_id = credentials.user_id
        GROUP BY username
        ORDER BY score DESC, timestamp ASC
        LIMIT 10
    '''

    GET_USER_SCORES_BY_USERNAME = '''
        SELECT timestamp, score 
        FROM scores 
        INNER JOIN credentials ON scores.user_id = credentials.user_id
        WHERE username = ?
        ORDER BY timestamp DESC
    '''

    UPDATE_ADMIN_PASSWORD = '''
        UPDATE credentials 
        SET password = ?, isPasswordChanged = ? 
        WHERE username = ?
    '''

    DELETE_USER_BY_EMAIL = 'DELETE FROM users WHERE email = ?'

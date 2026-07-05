import sqlite3

DB_NAME = "cake.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            address TEXT )
                         ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT,
            price INTEGER )
                        ''')
       

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,                     
            cake_code TEXT,                      
            date TEXT DEFAULT CURRENT_TIMESTAMP  )
                       ''')
    conn.commit()
     
    fill_initial_cakes() 


# =====================================================================
#  ОТДЕЛ ПОЛЬЗОВАТЕЛЕЙ (Все краны для таблицы 'users','orders')
# =====================================================================
    
def add_user(tg_id: int, name: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO users (tg_id, name) VALUES (?, ?)",
            (tg_id, name)
    )
        

def get_user(tg_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM users WHERE tg_id = ?", (tg_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    

def update_user_address(tg_id: int, address: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
           "UPDATE users SET address = ? WHERE tg_id = ?", 
            (address, tg_id)
        )
        conn.commit()


def get_user_address(tg_id: int) -> str | None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
       
        cursor.execute("SELECT address FROM users WHERE tg_id = ?", (tg_id,))
        row = cursor.fetchone()
        
        if row and row[0]:
            return row[0]
        return None



def add_order(user_id: int, cake_code: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, cake_code) VALUES (?, ?)",
            (user_id, cake_code)
        )
        conn.commit()



# =====================================================================
#  ОТДЕЛ ТОРТОВ (Все краны для таблицы 'cakes')
# =====================================================================
    
def fill_initial_cakes():
    initial_cakes = [
        ('strawberry', 'Торт «Клубничный бархат»', 1500),
        ('cupcakes', 'Капкейки (6 шт)', 900),
        ('bento', 'Bento-торт', 1000)
    ]

   
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT OR IGNORE INTO cakes (code, name, price)
        VALUES (?, ?, ?)
    ''', initial_cakes)

    

def get_all_cakes():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT code, name, price FROM cakes')
        cakes = cursor.fetchall()
        return cakes    
    

def get_cake_name(cake_code: str) -> str:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM cakes WHERE code = ?", (cake_code,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return "DESSERT"



if __name__ == "__main__":
    init_db()    
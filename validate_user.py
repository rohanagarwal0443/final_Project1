import mysql.connector

# Directly put your Railway DB credentials here
DB_HOST = "shinkansen.proxy.rlwy.net"
DB_PORT = 58873
DB_USER = "root"
DB_PASSWORD = "JmEtaPRDZyiyXIUmsCEPDotxGNTUoZfp"
DB_NAME = "railway"
 
try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        print("Database connected successfully!")
except mysql.connector.Error as e:
        print("Database connection failed:", e)
        conn = None
        cursor = None

    # Login function
def login(data: tuple):
        if cursor is None:
            print("No database connection")
            return False
        try:
            q = "SELECT * FROM users_logins1 WHERE email=%s AND password=%s"
            cursor.execute(q, data)
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    # Signup function
def signup(data: tuple):
        if cursor is None:
            print("No database connection")
            return False
        try:
            sub_data = data[1:3]  # (email, password)
            if not login(sub_data):
                q = "INSERT INTO users_logins1 (name, email, password, phone) VALUES (%s, %s, %s, %s)"
                cursor.execute(q, data)
                conn.commit()
                if cursor.rowcount > 0:
                    return True
            else:
                return False
        except Exception as e:
            print(e)

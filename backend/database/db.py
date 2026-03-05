import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="felix55",   
)

cursor = conn.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS workflow_automation")
cursor.execute("USE workflow_automation")


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('admin','user') DEFAULT 'user',
    status ENUM('active','inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

print("Database and table created successfully!")

conn.commit()
cursor.close()
conn.close()

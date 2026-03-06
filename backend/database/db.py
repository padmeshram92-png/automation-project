

import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="felix55"
    )

    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS workflow_automation")
    cursor.execute("USE workflow_automation")

    # Users table
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

    # Workflows table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflows (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT,
        prompt TEXT,
        trigger_type VARCHAR(100),
        ai_step VARCHAR(100),
        action_type VARCHAR(100),
        status VARCHAR(50) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Rules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        workflow_id BIGINT NOT NULL,
        rule_name VARCHAR(255),
        condition TEXT NOT NULL,
        action TEXT NOT NULL,
        priority INT DEFAULT 0,
        status ENUM('active','inactive') DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (workflow_id) REFERENCES workflows(id)
    )
    """)

    # Rule Fallbacks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rule_fallbacks (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        rule_id BIGINT NOT NULL,
        fallback_action TEXT NOT NULL,
        fallback_type ENUM('api','llm','manual','webhook') DEFAULT 'api',
        retry_count INT DEFAULT 3,
        status ENUM('active','inactive') DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rule_id) REFERENCES rules(id)
    )
    """)

    # LLM Configurations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS llm_configs (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        workflow_id BIGINT,
        model_name VARCHAR(255),
        api_key VARCHAR(500),
        endpoint VARCHAR(500),
        temperature FLOAT DEFAULT 0.7,
        max_tokens INT DEFAULT 2048,
        status ENUM('active','inactive') DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (workflow_id) REFERENCES workflows(id)
    )
    """)

    # API Integrations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_integrations (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        workflow_id BIGINT,
        api_name VARCHAR(255),
        endpoint VARCHAR(500),
        api_key VARCHAR(500),
        auth_type ENUM('bearer','apikey','basic','oauth') DEFAULT 'apikey',
        headers JSON,
        status ENUM('active','inactive') DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (workflow_id) REFERENCES workflows(id)
    )
    """)

    # Workflow Executions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executions (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        workflow_id BIGINT NOT NULL,
        trigger_data JSON,
        ai_response TEXT,
        action_result TEXT,
        status ENUM('success','failed','pending','fallback_used') DEFAULT 'pending',
        error_message TEXT,
        execution_time_ms INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (workflow_id) REFERENCES workflows(id)
    )
    """)

    # Audit Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT,
        action VARCHAR(255),
        entity_type VARCHAR(100),
        entity_id BIGINT,
        old_values JSON,
        new_values JSON,
        ip_address VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    print("✓ Database and all tables created successfully!")

except Error as err:
    print(f"Error: {err}")
finally:
    try:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    except:
        pass


def get_db_connection():
    """
    Get a database connection
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="felix55",
            database="workflow_automation"
        )
        return connection
    except Error as e:
        print(f"Warning: Could not connect to database: {e}")
        print("Running without database - some features may not work")
        return None


def get_connection():
    """
    Alias for get_db_connection for backward compatibility
    """
    return get_db_connection()

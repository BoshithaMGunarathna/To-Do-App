"""
Database configuration and connection management.
Follows Single Responsibility Principle (SRP).
"""
import mysql.connector
from mysql.connector import MySQLConnection
import time
import os
from typing import Optional


class DatabaseConfig:
    """Database configuration holder."""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'mysql_db')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'root')
        self.database = os.getenv('DB_NAME', 'todo_db')
        self.port = int(os.getenv('DB_PORT', '3306'))


class DatabaseConnection:
    """
    Database connection manager with retry logic.
    Follows Single Responsibility Principle (SRP).
    """
    
    def __init__(self, config: DatabaseConfig, max_retries: int = 5, retry_delay: int = 5):
        """
        Initialize database connection manager.
        
        Args:
            config: Database configuration
            max_retries: Maximum number of connection attempts
            retry_delay: Delay between retries in seconds
        """
        self.config = config
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._connection: Optional[MySQLConnection] = None
    
    def connect(self) -> MySQLConnection:
        """
        Establish database connection with retry logic.
        
        Returns:
            MySQL connection object
            
        Raises:
            Exception: If connection fails after all retries
        """
        retries = self.max_retries
        last_error = None
        
        while retries > 0:
            try:
                self._connection = mysql.connector.connect(
                    host=self.config.host,
                    user=self.config.user,
                    password=self.config.password,
                    database=self.config.database,
                    port=self.config.port
                )
                print(f"Successfully connected to database at {self.config.host}")
                return self._connection
            except mysql.connector.Error as err:
                last_error = err
                print(f"Database connection failed: {err}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying in {self.retry_delay} seconds... ({retries} attempts left)")
                    time.sleep(self.retry_delay)
        
        error_msg = f"Could not connect to database after {self.max_retries} attempts"
        if last_error:
            error_msg += f": {last_error}"
        raise Exception(error_msg)
    
    def get_connection(self) -> MySQLConnection:
        """
        Get the current database connection.
        Creates a new connection if one doesn't exist.
        
        Returns:
            MySQL connection object
        """
        if self._connection is None or not self._connection.is_connected():
            self.connect()
        return self._connection
    
    def close(self):
        """Close the database connection."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed")
    
    def reconnect(self) -> MySQLConnection:
        """
        Reconnect to the database.
        
        Returns:
            MySQL connection object
        """
        self.close()
        return self.connect()

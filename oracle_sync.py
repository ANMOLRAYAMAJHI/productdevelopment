"""
Oracle Database Sync Module
Automatically syncs data from SQLite to Oracle database
"""

from datetime import datetime
from config import Config
from sqlalchemy import create_engine

class OracleSync:
    """Handle syncing data to Oracle database"""
    
    def __init__(self):
        self.enabled = Config.ORACLE_ENABLED
        self.connection = None
        self.cursor = None
        self.sqlalchemy_uri = None
        self.engine = None
    
    def get_sqlalchemy_uri(self):
        """Build SQLAlchemy Oracle URI from configuration."""
        if Config.ORACLE_DB_URI:
            return Config.ORACLE_DB_URI
        return (
            f'oracle+oracledb://{Config.ORACLE_USER}:{Config.ORACLE_PASSWORD}@{Config.ORACLE_HOST}:{Config.ORACLE_PORT}/'
            f'?service_name={Config.ORACLE_SERVICE}'
        )

    def connect(self):
        """Establish connection to Oracle database"""
        if not self.enabled:
            return False
        try:
            import oracledb
        except Exception as e:
            print(f"⚠️  oracledb not available: {e}")
            self.enabled = False
            return False

        try:
            # Attempt to initialize thick client if available
            try:
                oracledb.init_oracle_client()
            except Exception:
                pass

            self.connection = oracledb.connect(
                user=Config.ORACLE_USER,
                password=Config.ORACLE_PASSWORD,
                host=Config.ORACLE_HOST,
                port=int(Config.ORACLE_PORT),
                service_name=Config.ORACLE_SERVICE
            )
            self.cursor = self.connection.cursor()
            self.sqlalchemy_uri = self.get_sqlalchemy_uri()
            self.engine = create_engine(self.sqlalchemy_uri)
            print("Connected to Oracle database for sync")
            return True
        except Exception as e:
            print(f"Oracle sync unavailable: {e}")
            self.enabled = False
            return False

    def ensure_schema(self):
        """Create Oracle tables if they do not already exist."""
        if not self.enabled or not self.engine:
            return False
        try:
            from models import db
            db.metadata.create_all(self.engine)
            print("Oracle schema verified/created")
            return True
        except Exception as e:
            print(f"Failed to create Oracle schema: {e}")
            return False
    
    def sync_admin(self, admin_id, username, password_hash):
        """Sync admin to Oracle"""
        if not self.enabled or not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                MERGE INTO HELPDESK_ADMIN ha
                USING (SELECT :admin_id as aid, :username as uname FROM DUAL) src
                ON (ha.ADMIN_ID = src.aid)
                WHEN MATCHED THEN
                    UPDATE SET ha.USERNAME = src.uname, ha.PASSWORD = :password, ha.UPDATED_DATE = SYSDATE
                WHEN NOT MATCHED THEN
                    INSERT (ADMIN_ID, USERNAME, PASSWORD, CREATED_DATE, UPDATED_DATE)
                    VALUES (src.aid, src.uname, :password, SYSDATE, SYSDATE)
            """, {'admin_id': admin_id, 'username': username, 'password': password_hash})
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"⚠️  Failed to sync admin: {e}")
            return False
    
    def sync_ticket(self, ticket_data):
        """Sync ticket to Oracle"""
        if not self.enabled or not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                MERGE INTO HELPDESK_TICKET ht
                USING (SELECT :ticket_id as tid FROM DUAL) src
                ON (ht.TICKET_ID = src.tid)
                WHEN MATCHED THEN
                    UPDATE SET 
                        ht.STATUS = :status,
                        ht.SENTIMENT = :sentiment,
                        ht.PRIORITY = :priority,
                        ht.UPDATED_DATE = SYSDATE
                WHEN NOT MATCHED THEN
                    INSERT (TICKET_ID, CUSTOMER_NAME, EMAIL, CATEGORY, SUBJECT, MESSAGE, 
                            SENTIMENT, PRIORITY, STATUS, CREATED_DATE, UPDATED_DATE, ADMIN_ID)
                    VALUES (:ticket_id, :customer_name, :email, :category, :subject, :message,
                            :sentiment, :priority, :status, SYSDATE, SYSDATE, :admin_id)
            """, ticket_data)
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"⚠️  Failed to sync ticket: {e}")
            return False
    
    def get_oracle_stats(self):
        """Get statistics from Oracle for reporting"""
        if not self.enabled or not self.cursor:
            return None
        
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_tickets,
                    SUM(CASE WHEN STATUS = 'Open' THEN 1 ELSE 0 END) as open_tickets,
                    SUM(CASE WHEN STATUS = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                    SUM(CASE WHEN STATUS = 'Closed' THEN 1 ELSE 0 END) as closed_tickets
                FROM HELPDESK_TICKET
            """)
            
            result = self.cursor.fetchone()
            return {
                'total': result[0] or 0,
                'open': result[1] or 0,
                'in_progress': result[2] or 0,
                'closed': result[3] or 0
            }
        except:
            return None
    
    def close(self):
        """Close Oracle connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Global instance
oracle_sync = OracleSync()

def init_oracle_sync(app=None):
    """Initialize Oracle sync on app startup"""
    if app:
        if oracle_sync.connect():
            oracle_sync.ensure_schema()

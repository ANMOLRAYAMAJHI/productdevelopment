"""
Oracle Database Sync Module
Automatically syncs data from SQLite to Oracle database
"""

import oracledb
from datetime import datetime
from config import Config

class OracleSync:
    """Handle syncing data to Oracle database"""
    
    def __init__(self):
        self.enabled = Config.ORACLE_ENABLED
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Oracle database"""
        if not self.enabled:
            return False
        
        try:
            # Thick mode connection using TNS entry
            oracledb.init_oracle_client()
        except:
            pass
        
        try:
            self.connection = oracledb.connect(
                user=Config.ORACLE_USER,
                password=Config.ORACLE_PASSWORD,
                host=Config.ORACLE_HOST,
                port=int(Config.ORACLE_PORT),
                service_name=Config.ORACLE_SERVICE
            )
            self.cursor = self.connection.cursor()
            print("✅ Connected to Oracle database for sync")
            return True
        except Exception as e:
            print(f"⚠️  Oracle sync unavailable: {e}")
            self.enabled = False
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
        oracle_sync.connect()

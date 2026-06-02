"""
Migration script to backup and transfer data from SQLite to Oracle database
Usage: python migrate_to_oracle.py
"""

import sqlite3
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Admin, Ticket, db

def backup_sqlite():
    """Backup SQLite database before migration"""
    db_path = 'database/helpdesk.db'
    if os.path.exists(db_path):
        backup_path = f'database/helpdesk_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        with open(db_path, 'rb') as f:
            data = f.read()
        with open(backup_path, 'wb') as f:
            f.write(data)
        print(f"✅ SQLite backup created: {backup_path}")
        return True
    return False

def migrate_data():
    """Migrate data from SQLite to Oracle"""
    sqlite_path = 'database/helpdesk.db'
    
    if not os.path.exists(sqlite_path):
        print("❌ SQLite database not found. No data to migrate.")
        return False
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to Oracle
        from app import create_app
        app = create_app('production')
        
        with app.app_context():
            # Migrate Admin data
            sqlite_cursor.execute("SELECT * FROM admin")
            admins = sqlite_cursor.fetchall()
            
            migrated_admins = 0
            for admin_row in admins:
                try:
                    admin = Admin(
                        username=admin_row['username'],
                        created_date=admin_row['created_date']
                    )
                    admin.set_password(admin_row['password'])
                    db.session.add(admin)
                    migrated_admins += 1
                except Exception as e:
                    print(f"⚠️  Error migrating admin {admin_row['username']}: {e}")
            
            # Migrate Ticket data
            sqlite_cursor.execute("SELECT * FROM ticket")
            tickets = sqlite_cursor.fetchall()
            
            migrated_tickets = 0
            for ticket_row in tickets:
                try:
                    ticket = Ticket(
                        customer_name=ticket_row['customer_name'],
                        email=ticket_row['email'],
                        category=ticket_row['category'],
                        subject=ticket_row['subject'],
                        message=ticket_row['message'],
                        sentiment=ticket_row['sentiment'],
                        priority=ticket_row['priority'],
                        status=ticket_row['status'],
                        created_date=ticket_row['created_date'],
                        updated_date=ticket_row['updated_date'],
                        admin_id=ticket_row['admin_id']
                    )
                    db.session.add(ticket)
                    migrated_tickets += 1
                except Exception as e:
                    print(f"⚠️  Error migrating ticket {ticket_row['customer_name']}: {e}")
            
            # Commit all changes
            db.session.commit()
            sqlite_conn.close()
            
            print(f"\n✅ Migration completed successfully!")
            print(f"   - Admins migrated: {migrated_admins}")
            print(f"   - Tickets migrated: {migrated_tickets}")
            return True
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    print("=" * 60)
    print("SQLite to Oracle Migration Tool")
    print("=" * 60)
    
    # Step 1: Backup SQLite
    print("\n1️⃣  Creating SQLite backup...")
    backup_sqlite()
    
    # Step 2: Migrate data
    print("\n2️⃣  Migrating data to Oracle...")
    if migrate_data():
        print("\n✅ All systems ready! Your Oracle database is now synced.")
        print("   Run 'python app.py' to start the Flask app with Oracle backend.")
    else:
        print("\n⚠️  Migration encountered issues. Please check the errors above.")

if __name__ == '__main__':
    main()

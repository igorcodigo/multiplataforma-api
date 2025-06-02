import os
import shutil
import datetime
import tempfile
import zipfile
from pathlib import Path
from django.core.management.base import BaseCommand
from email_service.backup_email import send_backup_email


class Command(BaseCommand):
    help = 'Backup the SQLite database and send it via email'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database backup process...'))
        success = self.backup_sqlite_database()
        if success:
            self.stdout.write(self.style.SUCCESS('Database backup completed successfully.'))
        else:
            self.stdout.write(self.style.ERROR('Database backup failed.'))

    def backup_sqlite_database(self):
        """
        Create a backup of the SQLite database and send it via email.
        """
        # Get configuration from environment variables or use defaults
        db_path = os.getenv('DB_PATH', 'db.sqlite3')
        backup_dir = os.getenv('BACKUP_DIR', 'backups')
        email_receiver = os.getenv('EMAIL_RECEIVER', 'youremail@example.com')
        email_sender = os.getenv('EMAIL_SENDER', 'no-reply@example.com')
        
        # Create the backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate timestamp for the backup file
        timestamp = datetime.datetime.now().strftime('%d_%m_%Y_%H:%M')
        backup_filename = f"db_backup_{timestamp}.sqlite3"
        zip_filename = f"db_backup_{timestamp}.zip"
        
        # Path to the database file
        db_file = Path(db_path)
        
        # Validate if the database file exists
        if not db_file.exists():
            self.stdout.write(self.style.ERROR(f"Error: Database file not found at {db_file}"))
            return False
        
        # Create a temporary directory for the backup
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            backup_file = temp_path / backup_filename
            zip_file = temp_path / zip_filename
            
            # Copy the database file to the backup file
            try:
                shutil.copy2(db_file, backup_file)
                self.stdout.write(self.style.SUCCESS(f"Database backup created at {backup_file}"))
                
                # Create a zip file containing the backup
                with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(backup_file, arcname=backup_filename)
                
                self.stdout.write(self.style.SUCCESS(f"Backup compressed as {zip_file}"))
                
                # Save a copy to the backup directory
                shutil.copy2(zip_file, Path(backup_dir) / zip_filename)
                self.stdout.write(self.style.SUCCESS(f"Backup saved to {backup_dir}/{zip_filename}"))
                
                # Send the backup via email using the email service
                result = send_backup_email(str(zip_file), email_sender, email_receiver, timestamp)
                if result:
                    self.stdout.write(self.style.SUCCESS(f"Backup email sent to {email_receiver}"))
                else:
                    self.stdout.write(self.style.ERROR("Failed to send backup email"))
                    
                return True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during backup process: {e}"))
                return False 
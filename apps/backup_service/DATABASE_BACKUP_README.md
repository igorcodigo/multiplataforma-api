# Database Backup System

This is a simple SQLite database backup system that creates backups of your database and sends them via email using Resend's SMTP service.

## Architecture

The backup system is organized according to the separation of concerns principle:

- **Backup Service**: Located in `backup_service/management/commands/backup_db.py` - A dedicated service for database backups
- **Email Service**: Located in `email_service/backup_email.py` - Handles sending emails with backup attachments

## Features

- Creates a timestamped backup of the SQLite database
- Compresses the backup into a ZIP file
- Stores backups in a local directory
- Sends the backup via email using Resend SMTP
- Available as a Django management command

## Configuration

The backup system uses the following environment variables, which can be set in your `.env` file:

- `DB_PATH`: Path to the SQLite database (default: "db.sqlite3")
- `BACKUP_DIR`: Directory to store backups (default: "backups")
- `EMAIL_RECEIVER`: Email address to receive the backup
- `EMAIL_SENDER`: Email address used as the sender
- `RESEND_API_KEY`: Your Resend API key for SMTP authentication
- `RESEND_SMTP_HOST`: Resend SMTP host (default: "smtp.resend.com")
- `RESEND_SMTP_PORT`: Resend SMTP port (default: 587)
- `RESEND_SMTP_USERNAME`: Resend SMTP username (default: "resend")

Example `.env` configuration:

```
RESEND_API_KEY=re_123456789
RESEND_SMTP_PORT=587
RESEND_SMTP_USERNAME=resend
RESEND_SMTP_HOST=smtp.resend.com
EMAIL_RECEIVER=your-email@example.com
EMAIL_SENDER=no-reply@yourdomain.com
DB_PATH=db.sqlite3
BACKUP_DIR=backups
```

## How to Use

### Using the Django Management Command

Run the backup from the command line:

```
python manage.py backup_db
```

### Using the Batch Script

Run the batch script:

```
z_automacoes_igor\backup_database.bat
```

## Scheduling Backups

### Windows Task Scheduler

1. Open Task Scheduler
2. Create a new Basic Task
3. Name it "SQLite Database Backup"
4. Set the trigger (daily, weekly, etc.)
5. Choose "Start a Program"
6. Browse to the location of your batch file
7. Finish the wizard

### Linux Cron Job

Add a line to your crontab:

```
0 3 * * * cd /path/to/your/project && python manage.py backup_db
```

This will run the backup every day at 3 AM.

## Troubleshooting

- **Email not sending**: Check your Resend API key and email configuration
- **Database file not found**: Verify the path to your SQLite database
- **Permission errors**: Ensure your user has permission to read the database and write to the backup directory 
import os
import datetime

# Try to import Django settings, but handle the case when running standalone
try:
    from django.conf import settings
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False

from .email_utils import (
    load_email_template, 
    customize_template, 
    send_email
)

def get_email_content(timestamp):
    """
    Get email content based on language settings.
    
    Args:
        timestamp (str): Timestamp of the backup for email subject
        
    Returns:
        dict: Dictionary containing email content elements
    """
    # Get language from settings or use default
    if DJANGO_AVAILABLE:
        try:
            language = getattr(settings, 'LANGUAGE_CODE', 'en').lower()
        except:
            language = 'en'
    else:
        language = 'en'
    
    # Email content based on language
    if language.startswith('pt'):
        return {
            'title': "Backup do Banco de Dados",
            'subject': f"Backup do Banco de Dados SQLite - {timestamp}",
            'main_text': f"Segue em anexo o backup do banco de dados de {timestamp}.",
            'footer_text': "Esta é uma mensagem automática. Por favor, não responda."
        }
    else:
        return {
            'title': "Database Backup",
            'subject': f"SQLite Database Backup - {timestamp}",
            'main_text': f"Please find attached the database backup from {timestamp}.",
            'footer_text': "This is an automated message. Please do not reply."
        }

def get_email_template(content):
    """
    Get email HTML template and populate it with content.
    
    Args:
        content (dict): Dictionary containing email content elements
        
    Returns:
        str: HTML content for the email
    """
    try:
        # Try to load template using utility function
        template_content = load_email_template('backup_email_template')
        
        # Use utility function to customize template
        replacements = {
            'title': content['title'],
            'main_text': content['main_text'],
            'footer_text': content['footer_text']
        }
        return customize_template(template_content, replacements)
    except Exception as e:
        print(f"Error loading template: {e}")
        # Fallback to simple HTML
        return f"""
        <html>
        <body>
            <h2>{content['title']}</h2>
            <p>{content['main_text']}</p>
            <p>{content['footer_text']}</p>
        </body>
        </html>
        """


def send_backup_email(zip_file_path, to_email, timestamp, from_email="no-reply@assistenteelio.com.br"):



    """
    Send the backup file via email using Resend API.
    
    Args:
        zip_file_path (str): Path to the zip file containing the backup
        to_email (str): Recipient email address
        timestamp (str): Timestamp of the backup for email subject
        from_email (str): Sender email address
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Verify file exists
        if not os.path.exists(zip_file_path):
            print(f"Error: Backup file not found at {zip_file_path}")
            return False
            
        # Get email content
        content = get_email_content(timestamp)
        
        # Get email template
        html_content = get_email_template(content)
        
        # Create attachment data
        attachments = [{
            "filename": os.path.basename(zip_file_path),
            "path": zip_file_path
        }]
        
        # Send email using Resend API
        response = send_email(
            to_email=to_email,
            subject=content['subject'],
            html_content=html_content,
            from_email=from_email,
            attachments=attachments
        )
        
        # Check if email was sent successfully
        if response and 'id' in response:
            print(f"Backup email sent successfully, ID: {response['id']}")
            return True
        else:
            print(f"Error sending backup email: Unexpected response from Resend API")
            return False
            
    except Exception as e:
        print(f"Error sending backup email: {e}")
        import traceback
        traceback.print_exc()
        return False 
    

# Generate a default timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
send_backup_email(
    zip_file_path=r"C:\Users\igor1\Desktop\Subarashii_Code\Template-Django2\email_service\templates\password_reset_template.html",
    to_email="igor123cf@gmail.com",
    timestamp=timestamp
)

import os
import resend
from dotenv import load_dotenv
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import base64

# Load environment variables
load_dotenv()

# Get the current directory to facilitate file path connections
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get API key from .env file
resend.api_key = os.getenv('RESEND_API_KEY')

def validate_api_key():
    """Verifies if the API key is properly configured."""
    if not resend.api_key:
        raise ValueError("Error: RESEND_API_KEY not found in .env file")

def load_email_template(template_name):
    """
    Loads an HTML template file.
    
    Args:
        template_name (str): Template file name without extension
        
    Returns:
        str: Content of the HTML file
    """
    template_path = os.path.join(current_directory, 'templates', f'{template_name}.html')
    
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def customize_template(template_content, replacements):
    """
    Replaces placeholders in the template with actual values.
    
    Args:
        template_content (str): HTML template content
        replacements (dict): Dictionary with values to replace
        
    Returns:
        str: Customized HTML template
    """
    content = template_content
    for placeholder, value in replacements.items():
        content = content.replace(f'{{{{ {placeholder} }}}}', value)
    return content

def create_email_connection():
    """
    Create and return an email connection using Resend SMTP settings.
    
    Returns:
        object: Email connection object
    """
    return get_connection(
        host=settings.RESEND_SMTP_HOST,
        port=settings.RESEND_SMTP_PORT,
        username=settings.RESEND_SMTP_USERNAME,
        password=os.getenv('RESEND_API_KEY', ''),
        use_tls=True,
    )

def create_email_message(subject, html_content, from_email, to_email, connection):
    """
    Create an EmailMessage object.
    
    Args:
        subject (str): Email subject
        html_content (str): HTML content for the email
        from_email (str): Sender email address
        to_email (str): Recipient email address
        connection: Email connection object
        
    Returns:
        EmailMessage: Configured email message object
    """
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=from_email,
        to=[to_email],
        connection=connection,
    )
    
    # Set email type as HTML
    email.content_subtype = "html"
    return email

def attach_file(email, file_path, mime_type=None):
    """
    Attach a file to the email if it exists.
    
    Args:
        email (EmailMessage): Email message object
        file_path (str): Path to the file to attach
        mime_type (str, optional): MIME type of the file. If None, will be guessed based on extension.
        
    Returns:
        bool: True if file was attached successfully, False otherwise
    """
    if os.path.exists(file_path):
        if mime_type is None:
            # Try to guess mime type from extension
            file_extension = os.path.splitext(file_path)[1].lower()
            mime_map = {
                '.zip': 'application/zip',
                '.pdf': 'application/pdf',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.txt': 'text/plain',
                '.csv': 'text/csv',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            mime_type = mime_map.get(file_extension, 'application/octet-stream')
            
        with open(file_path, 'rb') as f:
            email.attach(os.path.basename(file_path), f.read(), mime_type)
        return True
    return False

def send_email(to_email, subject, html_content, from_email="no-reply@assistenteelio.com.br", attachments=None):
    """
    Sends an email using Resend API with optional attachments.
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        html_content (str): HTML email content
        from_email (str): Sender email
        attachments (list, optional): List of dictionaries with file details to attach
                                     Example: [{"filename": "file.pdf", "path": "/path/to/file.pdf"}]
        
    Returns:
        dict: Resend API response
    """
    try:
        email_data = {
            "from": from_email,
            "to": [to_email] if isinstance(to_email, str) else to_email,
            "subject": subject,
            "html": html_content
        }
        
        # Add attachments if provided
        if attachments:
            email_data["attachments"] = []
            for attachment in attachments:
                if "path" in attachment and os.path.exists(attachment["path"]):
                    with open(attachment["path"], "rb") as file:
                        file_content = file.read()
                        file_base64 = base64.b64encode(file_content).decode("utf-8")
                        
                        filename = attachment.get("filename", os.path.basename(attachment["path"]))
                        
                        email_data["attachments"].append({
                            "filename": filename,
                            "content": file_base64
                        })
        
        response = resend.Emails.send(email_data)
        return response
    except Exception as e:
        raise Exception(f"Error sending email: {e}") 
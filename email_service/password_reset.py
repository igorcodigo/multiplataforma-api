import os
import urllib.parse
from .email_utils import validate_api_key, load_email_template, send_email

# Get APP_EXCLUSIVE from environment variables
app_exclusive = os.getenv('APP_EXCLUSIVE', 'False').strip().lower() in ('1', 'true', 'yes')

def extract_reset_code(reset_url):
    """Extracts reset code from URL"""
    parsed_url = urllib.parse.urlparse(reset_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return query_params.get('code', [''])[0]

def prepare_html_content(html_content, reset_code, reset_url):
    """Prepares HTML content with specific data"""
    # Replace code placeholder
    html_content = html_content.replace('{{ reset_code }}', reset_code)
    
    # Conditional to include or not the reset button and link
    if app_exclusive:
        # If app exclusive, remove button and link
        html_content = html_content.replace('{{ RESET_BUTTON_PLACEHOLDER }}', '')
        html_content = html_content.replace('{{ RESET_LINK_PLACEHOLDER }}', '')
    else:
        # If not app exclusive, include button and link
        reset_button = f'<div style="text-align: center;"><a href="{reset_url}" style="display: inline-block; padding: 10px 20px; margin: 20px 0; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Redefinir Senha</a></div>'
        reset_link = f'<p>Ou copie e cole o seguinte link no seu navegador:</p><p style="word-break: break-all;">{reset_url}</p>'
        
        html_content = html_content.replace('{{ RESET_BUTTON_PLACEHOLDER }}', reset_button)
        html_content = html_content.replace('{{ RESET_LINK_PLACEHOLDER }}', reset_link)
    
    return html_content

def send_password_reset_email(email, reset_url):
    """
    Sends a password recovery email to the user.
    
    Args:
        email (str): User email address
        reset_url (str): URL to reset password
    
    Returns:
        dict: Resend API response
    """
    # Validate API key
    validate_api_key()
    
    # Extract reset code from URL
    #reset_code = extract_reset_code(reset_url)

    reset_code = "123456"
    
    # Load HTML template
    html_content = load_email_template('password_reset_template')
    
    # Prepare HTML content with specific data
    html_content = prepare_html_content(html_content, reset_code, reset_url)
    
    # Send email
    return send_email(
        to_email=email,
        subject="Recuperação de Senha",
        html_content=html_content
    ) 

send_password_reset_email("igor123cf@gmail.com", "https://www.google.com")
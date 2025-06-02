import os
from .email_utils import validate_api_key, load_email_template, customize_template, send_email

def send_welcome_email(email, name):
    """
    Sends a welcome email to a newly registered user.
    
    Args:
        email (str): User email address
        name (str): User name
    
    Returns:
        dict: Resend API response
    """
    # Validate API key
    validate_api_key()
    
    # Load template
    template_content = load_email_template('welcome_template')
    
    # Customize template
    html_content = customize_template(template_content, {'name': name})
    
    # Send email
    return send_email(
        to_email=email,
        subject="Bem-vindo(a) à nossa plataforma!",
        html_content=html_content
    ) 

send_welcome_email("igor123cf@gmail.com", "Igor")
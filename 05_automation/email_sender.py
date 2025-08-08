#!/usr/bin/env python3
"""
Email Sender - Automated Email Sending Script

This script provides functionality to send automated emails with support for:
- Plain text and HTML emails
- File attachments
- Multiple recipients
- Email templates
- SMTP configuration for various providers

Author: Python Automation Examples
Date: 2025
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from pathlib import Path
from typing import List, Dict, Optional, Union
import json
import logging
from datetime import datetime
import argparse
import getpass


class EmailSender:
    """
    A class to handle automated email sending with various features.
    
    Attributes:
        smtp_server (str): SMTP server address
        smtp_port (int): SMTP server port
        username (str): Email account username
        password (str): Email account password
        use_tls (bool): Whether to use TLS encryption
    """
    
    # Common SMTP configurations
    SMTP_CONFIGS = {
        'gmail': {
            'server': 'smtp.gmail.com',
            'port': 587,
            'tls': True
        },
        'outlook': {
            'server': 'smtp-mail.outlook.com',
            'port': 587,
            'tls': True
        },
        'yahoo': {
            'server': 'smtp.mail.yahoo.com',
            'port': 587,
            'tls': True
        },
        'icloud': {
            'server': 'smtp.mail.me.com',
            'port': 587,
            'tls': True
        }
    }
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, 
                 password: str, use_tls: bool = True):
        """
        Initialize the EmailSender.
        
        Args:
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port
            username (str): Email username
            password (str): Email password
            use_tls (bool): Whether to use TLS encryption
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        
        self._setup_logging()
    
    @classmethod
    def from_provider(cls, provider: str, username: str, password: str):
        """
        Create EmailSender instance using predefined provider settings.
        
        Args:
            provider (str): Email provider ('gmail', 'outlook', 'yahoo', 'icloud')
            username (str): Email username
            password (str): Email password
            
        Returns:
            EmailSender: Configured EmailSender instance
        """
        if provider.lower() not in cls.SMTP_CONFIGS:
            raise ValueError(f"Unsupported provider: {provider}")
        
        config = cls.SMTP_CONFIGS[provider.lower()]
        return cls(
            smtp_server=config['server'],
            smtp_port=config['port'],
            username=username,
            password=password,
            use_tls=config['tls']
        )
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_sender.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, to_emails: Union[str, List[str]], subject: str, 
                   body: str, html_body: Optional[str] = None,
                   attachments: Optional[List[str]] = None,
                   cc_emails: Optional[List[str]] = None,
                   bcc_emails: Optional[List[str]] = None) -> bool:
        """
        Send an email with optional attachments.
        
        Args:
            to_emails: Recipient email(s) - single string or list
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
            attachments: List of file paths to attach
            cc_emails: List of CC recipients
            bcc_emails: List of BCC recipients
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['Subject'] = subject
            
            # Handle recipients
            if isinstance(to_emails, str):
                to_emails = [to_emails]
            msg['To'] = ', '.join(to_emails)
            
            # Handle CC
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
                to_emails.extend(cc_emails)
            
            # Handle BCC (don't add to headers, just to recipient list)
            if bcc_emails:
                to_emails.extend(bcc_emails)
            
            # Add body content
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if not Path(file_path).exists():
                        self.logger.warning(f"Attachment not found: {file_path}")
                        continue
                    
                    self._attach_file(msg, file_path)
            
            # Send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls(context=context)
                server.login(self.username, self.password)
                server.sendmail(self.username, to_emails, msg.as_string())
            
            self.logger.info(f"Email sent successfully to {len(to_emails)} recipient(s)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """
        Attach a file to the email message.
        
        Args:
            msg: Email message object
            file_path: Path to file to attach
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'rb') as attachment:
                # Determine if it's an image
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    part = MIMEImage(attachment.read())
                    part.add_header('Content-Disposition', f'attachment; filename= {file_path.name}')
                else:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.name}'
                    )
                
                msg.attach(part)
                self.logger.info(f"Attached file: {file_path.name}")
                
        except Exception as e:
            self.logger.error(f"Failed to attach {file_path.name}: {str(e)}")
    
    def send_bulk_emails(self, email_list: List[Dict], template_file: Optional[str] = None) -> Dict[str, int]:
        """
        Send bulk emails using a list of email data.
        
        Args:
            email_list: List of dictionaries with email data
            template_file: Optional template file path
            
        Returns:
            Dict with success/failure counts
        """
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        # Load template if provided
        template = None
        if template_file and Path(template_file).exists():
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template = f.read()
            except Exception as e:
                self.logger.error(f"Failed to load template: {str(e)}")
        
        for email_data in email_list:
            try:
                # Extract email parameters
                to_email = email_data.get('to')
                subject = email_data.get('subject', 'No Subject')
                body = email_data.get('body', '')
                
                # Use template if available and substitute placeholders
                if template:
                    body = template
                    for key, value in email_data.items():
                        body = body.replace(f'{{{key}}}', str(value))
                
                # Send email
                if self.send_email(
                    to_emails=to_email,
                    subject=subject,
                    body=body,
                    html_body=email_data.get('html_body'),
                    attachments=email_data.get('attachments'),
                    cc_emails=email_data.get('cc'),
                    bcc_emails=email_data.get('bcc')
                ):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to send to {to_email}")
                    
            except Exception as e:
                results['failed'] += 1
                error_msg = f"Error processing email to {email_data.get('to', 'unknown')}: {str(e)}"
                results['errors'].append(error_msg)
                self.logger.error(error_msg)
        
        return results
    
    def test_connection(self) -> bool:
        """
        Test the SMTP connection and authentication.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls(context=context)
                server.login(self.username, self.password)
                self.logger.info("SMTP connection test successful")
                return True
                
        except Exception as e:
            self.logger.error(f"SMTP connection test failed: {str(e)}")
            return False


class EmailTemplate:
    """Helper class for managing email templates."""
    
    @staticmethod
    def create_html_template(title: str, content: str, footer: str = None) -> str:
        """
        Create a basic HTML email template.
        
        Args:
            title: Email title
            content: Main content
            footer: Optional footer text
            
        Returns:
            str: HTML template string
        """
        footer_html = f"<p style='font-size: 12px; color: #666;'>{footer}</p>" if footer else ""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    {title}
                </h1>
                <div style="margin: 20px 0;">
                    {content}
                </div>
                {footer_html}
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #999;">
                        Sent on {datetime.now().strftime('%Y-%m-%d at %H:%M')}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def save_template(template_content: str, filename: str):
        """Save template to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(template_content)
            print(f"Template saved to {filename}")
        except Exception as e:
            print(f"Error saving template: {str(e)}")


def load_email_config(config_file: str) -> Dict:
    """Load email configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}


def main():
    """Main function to handle command line email sending."""
    parser = argparse.ArgumentParser(description='Send automated emails')
    parser.add_argument('--config', help='JSON configuration file')
    parser.add_argument('--provider', choices=['gmail', 'outlook', 'yahoo', 'icloud'],
                       help='Email provider')
    parser.add_argument('--username', help='Email username')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--html-body', help='HTML email body')
    parser.add_argument('--attachments', nargs='*', help='File attachments')
    parser.add_argument('--template', help='Email template file')
    parser.add_argument('--test-connection', action='store_true',
                       help='Test SMTP connection only')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        if args.config:
            config = load_email_config(args.config)
            email_sender = EmailSender(**config)
        elif args.provider and args.username:
            password = getpass.getpass(f"Enter password for {args.username}: ")
            email_sender = EmailSender.from_provider(args.provider, args.username, password)
        else:
            print("Error: Either --config or --provider with --username is required")
            return 1
        
        # Test connection if requested
        if args.test_connection:
            if email_sender.test_connection():
                print("✅ Connection test successful!")
                return 0
            else:
                print("❌ Connection test failed!")
                return 1
        
        # Prepare email body
        body = args.body or "This is an automated email."
        if args.template and Path(args.template).exists():
            with open(args.template, 'r', encoding='utf-8') as f:
                body = f.read()
        
        # Send email
        success = email_sender.send_email(
            to_emails=args.to,
            subject=args.subject,
            body=body,
            html_body=args.html_body,
            attachments=args.attachments
        )
        
        if success:
            print("✅ Email sent successfully!")
            return 0
        else:
            print("❌ Failed to send email!")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Send simple email using Gmail:
       python email_sender.py --provider gmail --username your@gmail.com 
                             --to recipient@example.com --subject "Test Email" 
                             --body "Hello from Python!"
    
    2. Send email with attachments:
       python email_sender.py --provider gmail --username your@gmail.com 
                             --to recipient@example.com --subject "Files Attached" 
                             --attachments file1.pdf file2.jpg
    
    3. Send HTML email:
       python email_sender.py --provider outlook --username your@outlook.com 
                             --to recipient@example.com --subject "HTML Email" 
                             --html-body "<h1>Hello</h1><p>This is HTML!</p>"
    
    4. Test connection only:
       python email_sender.py --provider gmail --username your@gmail.com --test-connection
    
    5. Use configuration file:
       python email_sender.py --config email_config.json --to recipient@example.com 
                             --subject "Configured Email"
    
    Configuration file example (email_config.json):
    {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your@gmail.com",
        "password": "your_password",
        "use_tls": true
    }
    
    Bulk email example:
    email_list = [
        {
            "to": "person1@example.com",
            "subject": "Hello {name}",
            "name": "John",
            "body": "Hi {name}, this is a personalized message!"
        },
        {
            "to": "person2@example.com", 
            "subject": "Hello {name}",
            "name": "Jane",
            "body": "Hi {name}, this is a personalized message!"
        }
    ]
    
    sender = EmailSender.from_provider('gmail', 'your@gmail.com', 'password')
    results = sender.send_bulk_emails(email_list)
    """
    exit(main())
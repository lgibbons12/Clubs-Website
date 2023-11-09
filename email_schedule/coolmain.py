import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from display.models import Club

load_dotenv(encoding='utf-8')


def list_of_lists_to_html(list_of_lists):
    html_content = "<html><body>"

    for inner_list in list_of_lists:
        if len(inner_list) >= 2:
            # Format each inner list as a line with the first item bold and a colon before the second item
            line_html = f"<p><strong>{inner_list[0]}:</strong> {inner_list[1]}</p>"
            html_content += line_html

    html_content += "</body></html>"
    return html_content

def send_email():
    clubs = Club.objects.filter(approved=False)
    string = []
    for club in clubs:
        string.append([club.name, club.leaders])

    content = list_of_lists_to_html(string)
    message = Mail(
        from_email='cannonclubs@gmail.com',
        to_emails='lgibbons@cannonschool.org',
        subject='Unapproved Clubs',
        html_content="lW")

    try:
        sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        
        response = sg.send(message)
        print(f"Email sent successfully. Status Code: {response.status_code}")
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {str(e)}")


if __name__ == "__main__":
    send_email()
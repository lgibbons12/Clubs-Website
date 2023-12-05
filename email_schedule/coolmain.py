import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from display.models import Club
from blog.models import Post
load_dotenv(encoding='utf-8')



def list_of_lists_to_html(club_list, blog_list):
    html_content = "<html><body>"
    html_content += "<h1>Good morning! These are the current unapproved blog posts and clubs.</h1>"
    link = "http://127.0.0.1:8000/blog/approval/"
    html_content += f"<h2><a href='{link}'>Please click this link below to approve them!</a></h2>"

    
    for i in range(2):
        if i == 0:
            html_content += "<p><u>New/Edited Clubs:</u></p>"
            list_ = club_list
        elif i == 1:
            html_content += "<p><u>New Blog Posts:</u></p>"
            list_ = blog_list
        else:
            break
        for inner_list in list_:
            if len(inner_list) >= 2:
                # Format each inner list as a line with the first item bold and a colon before the second item
                if i == 0:
                    line_html = f"<p><strong>{inner_list[0]}:</strong> {inner_list[1]}</p>"
                elif i == 1:
                    pub_date = inner_list[2].strftime("%F %I:%M %p")
                    line_html = f"<p><strong>{inner_list[0]}:</strong> by {inner_list[1]} at {pub_date}</p>"
                html_content += line_html
    

    
    
    html_content += "</body></html>"
    return html_content

def send_email():
    
    clubs = Club.objects.filter(approved=False)
    club_list = []
    for club in clubs:
        club_list.append([club.name, club.leaders])
    
    posts = Post.objects.filter(approved = False)
    blog_list = []
    for post in posts:
        blog_list.append([post.name, post.club, post.pub_date])

    content = list_of_lists_to_html(club_list, blog_list)
    message = Mail(
        from_email='cannonclubs@gmail.com',
        to_emails='liamwgibbons@gmail.com',
        subject='Unapproved Clubs and Blog Posts Today',
        html_content=content)

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





    
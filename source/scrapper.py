from robobrowser import RoboBrowser

from bs4 import BeautifulSoup
import click
import sys 

def NetworkErrorClick():
    click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in', fg='red', bold=True))
    exit(0)


def attempt(user, password):
    url = 'http://erp.iitbbs.ac.in'
    browser = RoboBrowser(history=False, parser='html.parser')
    try:
        browser.open(url)
    except:
        NetworkErrorClick()

    try:
        form = browser.get_form(action='login.php')
    except:
        NetworkErrorClick()

    if not form:
        click.echo(click.style('Network error, Unable to fetch form \n', fg='red', bold=True))
        exit(0)

    
    form['email'].value = user
    form['password'].value = password

    try:
        browser.submit_form(form)
    except:
        NetworkErrorClick()

    if (browser.url != 'http://erp.iitbbs.ac.in/home.php'):
        return False

    attendance_link = 'http://erp.iitbbs.ac.in/biometric/list_students.php'

    try:
        browser.open(attendance_link)
    except:
        NetworkErrorClick()

    soup = BeautifulSoup(browser.response.text, 'html.parser')
    content = soup.find('div', attrs={'id': 'content'})
    table = content.find('table')

    tr = table.find_all('tr')
    result = dict()

    for row in tr[1:]: # Don't need headers
        td = row.find_all('td')
        code = td[0].text.strip()
        subject = td[1].text.strip()
        attended_class = td[2].text.strip()
        total_class = td[3].text.strip()
        percentage = td[4].text.strip()
        result[code] = {
            'code' : code,
            'name' : subject,
            'attended': attended_class,
            'total': total_class,
            'percentage': percentage
        }

    return result
from robobrowser import RoboBrowser

from bs4 import BeautifulSoup
import click
import sys 
import datetime
from tabulate import tabulate


def MissedClassDates(user, password, start = "2019-07-19"):
    
    url = 'http://erp.iitbbs.ac.in'
    browser = RoboBrowser(history=False, parser='html.parser')
    try:
        browser.open(url)
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0) 

    try:
        form = browser.get_form(action='login.php')
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0)

    if not form:
        click.echo(click.style('Network error, Unable to fetch form \n', fg='red', bold=True))
        exit(0)

    
    form['email'].value = user
    form['password'].value = password

    try:
        browser.submit_form(form)
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0)

    if (browser.url != 'http://erp.iitbbs.ac.in/home.php'):
        return False

    attendance_link = 'http://erp.iitbbs.ac.in/biometric/list_students_date_wise.php'

    try:
        browser.open(attendance_link)
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0)

    today = datetime.date.today() 

    start_date = start #start of semester 
    end_date = today.strftime("%Y-%m-%d")
    st = RangeOfDate(start_date, end_date)
    if len(st) == 0:
        return dict()
    StartdateIndex = 0
    EnddateIndex = len(st) - 1
    return ResponseTable(st, StartdateIndex, EnddateIndex,browser)

def RangeOfDate(startDate, EndDate):

    startDate = startDate.strip()
    start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end = datetime.datetime.strptime(EndDate, "%Y-%m-%d")
    if start >= end:
        return list()
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1) if (start + datetime.timedelta(days=x)).weekday() != 6]
    DateRange = [date.strftime("%Y-%m-%d") for date in date_generated]
    return DateRange

def ResponseTable(Dates, StartdateIndex, EnddateIndex, browser):
    result = dict()
    Startdate = Dates[StartdateIndex]
    Enddate = Dates[EnddateIndex]

    try:
        Date_form = browser.get_form(action='list_students_date_wise.php')
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0)

    Date_form['from'] = Startdate
    Date_form['to'] = Enddate

    try:
        browser.submit_form(Date_form)
    except:
        click.echo(click.style('Network error, please check your internet connection and firewall for URL: http://erp.iitbbs.ac.in \n', fg='red', bold=True))
        exit(0)

    Date_soup = BeautifulSoup(browser.response.text, 'html.parser')
    table = Date_soup.find('table', attrs={'border': '1'})

    tr = table.find_all('tr')
    if(Startdate != Enddate):
        total_class_attended = 0
        total_class_conducted = 0
        for row in tr[1:]:
            td = row.find_all('td')
            total_class_attended += int(td[2].text.strip())
            total_class_conducted += int(td[3].text.strip())
        if(total_class_attended != total_class_conducted):
            MidwayIndex = (StartdateIndex + EnddateIndex)//2
            result.update(ResponseTable(Dates, StartdateIndex, MidwayIndex, browser))
            result.update(ResponseTable(Dates, MidwayIndex+1, EnddateIndex, browser))
    else:
        result[Startdate] = list()
        for row in tr[1:]: # Don't need headers
            td = row.find_all('td')
            code = td[0].text.strip()
            subject = td[1].text.strip()
            attended_class = td[2].text.strip()
            total_class = td[3].text.strip()
            percentage = td[4].text.strip()
            if(total_class != attended_class):
                result[Startdate].append({
                'Date' :  Startdate,
                'code' : code,
                'subjectName' : subject,
                'attended': attended_class,
                'total': total_class,
                'percentage': percentage
                })

    return result
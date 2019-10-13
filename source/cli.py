import click
import keyring
import getpass
from source.scrapper import attempt
from tabulate import tabulate
from source.missedClassScrapper import MissedClassDates

@click.command()
@click.option('-r', '--roll', prompt='Roll Number', help='Enter the Roll Number for ERP Login.')
def attendance(roll):
    """
    Get the credentials first
    """
    password = keyring.get_password('ERP', roll)
    saved_password = True

    if password != None:
        response = attempt(roll, password)

        if not response:
            click.echo(click.style('Password modified, Enter new password.', fg='green', bold=True))
            keyring.delete_password('ERP',roll)
            password = None

    if password == None:
        password = getpass.getpass("Password : ")
        response,password = ResponseAttempt(roll,password)
        saved_password = False

    # Fetch attendance from ERP and Pretty Print it on Terminal.
    attendance_table = make_table(response)
    attendance_header = ["Subject Code","Subject Name", "Attended","Percentage"]
    show_table(attendance_table,attendance_header)

    # Fetch missed classes from ERP and Pretty Print it on Terminal.
    ans = input("Do you want to see the missed class(es) date-wise ? (y/N) ")
    if ans=='y':
        input_subject = []
        specific_class_ans = input("Do you want to see the missed class(es) of specific subject(s)? (y/N) ")
        if specific_class_ans=='y':
            input_subject = [x for x in input("Enter the Subject code(s) seperated by spaces: ").split()]

        print("please wait, it may take a while to fetch the information... \n")
        missed_class_response = MissedClassDates(roll,password)
        if specific_class_ans !='y':
             missed_class_table = make_missed_class_table(missed_class_response)
        else : 
            missed_class_table = make_specific_sub_missed_class_table(missed_class_response,input_subject)
        Missed_class_headers =  ["Date","Subject Name", "Attended"]
        show_table(missed_class_table,Missed_class_headers)

        
    # Store password locally if not saved already
    if not saved_password:
        ans = input("Do you want to store your password locally? (y/N) ")
        if ans=='y':
            keyring.set_password('ERP', roll, password)


def make_table(response):
    result = [[data['code'], data['name'], data['attended'] + '/' + data['total'],data['percentage']] for (code, data) in response.items()]
    return result

def make_missed_class_table(response):
    result  = [[data['Date'], data['subjectName'], data['attended'] + '/' + data['total']] for (Date, data) in response.items()]  
    return result

def make_specific_sub_missed_class_table(response,valid_subjectC_code):
    result = [[data['Date'], data['subjectName'], data['attended'] + '/' + data['total']] for (Date, data) in response.items() if(data['code'] in valid_subjectC_code)]
    return result

def ResponseAttempt(roll, password):

    response = attempt(roll, password)

    if not response:
        click.secho('Invalid Credentials, Sorry, try again', fg='red', bold=True)
        password = getpass.getpass("Password : ")
        response = attempt(roll, password)

    if not response:
        click.secho('Invalid Credentials, Sorry, try one more time.', fg='red', bold=True)
        password = getpass.getpass("Password : ")
        response = attempt(roll, password)

    if not response:
        click.secho('Invalid Credentials, 3 incorrect attempts', fg='red', bold=True)
        exit(0)

    return response,password


def show_table(table,table_headers):
    print(tabulate(table, headers=table_headers,tablefmt="fancy_grid"))





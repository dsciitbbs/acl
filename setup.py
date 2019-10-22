from setuptools import setup, find_packages

setup(
    name='acl-iitbbs',
    version='1.0',
    description='Fetch attendance from ERP and Pretty Print it on Terminal.',
    author='Aman Pratap Singh',
    author_email='amanprtpsingh@gmail.com',
    url='https://github.com/apsknight/acl',
    py_modules=['acl'],
    packages=find_packages(),
    install_requires=[
        'Click', 'robobrowser', 'bs4', 'tabulate', 'keyring'
    ],
    entry_points='''
        [console_scripts]
        acl=source:attendance
    ''',
)

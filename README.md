# ACL - Attendance on Command Line
> *Fetch attendance from ERP and Pretty Print it on Terminal.*

[![Build Status](https://travis-ci.com/dsciitbbs/acl.svg?branch=master)](https://travis-ci.com/dsciitbbs/acl)

[![asciicast](https://asciinema.org/a/nBapjGfxqwNxgQHXfYn6N6TpH.svg)](https://asciinema.org/a/nBapjGfxqwNxgQHXfYn6N6TpH)

## Install
```bash
python3 -m pip install acl-iitbbs
```

## Update
```bash
python3 -m pip install acl-iitbbs --upgrade
```

## Usage
```
$ acl --help
    Usage: acl [OPTIONS]

    Fetch attendance from IITBBS's ERP and Pretty Print it on Terminal.

    Options:
    -r, --roll TEXT      Enter the Roll Number for ERP Login.
    -p, --password TEXT  Enter Password for ERP Login.
    --help               Show this message and exit
```
```
$ acl --roll 16CS010XX
Password: 
╒═══════════════════════════════════════════════════╤════════════╤══════════════╕
│ Subject Name                                      │ Attended   │   Percentage │
╞═══════════════════════════════════════════════════╪════════════╪══════════════╡
│ Formal Languages and Automata Theory              │ 44/58      │        75.86 │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Computer Organization and Architecture            │ 38/49      │        77.55 │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Operating Systems                                 │ 30/47      │        63.83 │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Computer Organization and Architecture Laboratory │ 17/17      │       100    │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Operating Systems Laboratory                      │ 14/15      │        93.33 │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Numerical Methods                                 │ 52/66      │        78.79 │
├───────────────────────────────────────────────────┼────────────┼──────────────┤
│ Managerial Economics                              │ 25/42      │        59.52 │
╘═══════════════════════════════════════════════════╧════════════╧══════════════╛
```

## Contributors
- Aman Pratap Singh
- Tummala Madhav
- Aditya Pal
- Rahul Kumar
- Kaustav Bhattacharya

## License
MIT © [Aman Pratap Singh](https://aps.mit-license.org)

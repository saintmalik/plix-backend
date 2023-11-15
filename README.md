# Plixa [Backend]

✨ The open-source payment process that eliminates payment hurdles and receipt outage.

## Setup for development

This project uses `python3.11` and `pipenv` for managing project dependencies. if you don't have `pipenv` installed
globally, you can install it with
`pip install pipenv`.

Clone the repository

```bash
git clone https://github.com/saintmalik/plix-backend
```

Change directory to the cloned repository

```bash
cd plix-backend
```

Install the project dependencies

```bash
pipenv install
```

Activate the virtual environment shell

```bash
pipenv shell
```

Make migrations changes

```bash
python manage.py makemigrations
```

migrate the changes to the database

```bash
python manage.py migrate
```

Run the project

```bash
python manage.py runserver
```

## Design Goals

### Users End

- [x] No auth
- [] Click on make payment
- [] Make a full payment or half payment
- [] In payment dialogue, Enter Full name, phone number, matric number, level, and department/course
- [] Click payment and pay directly to the association account (transfer-based), I suggest mono or kora
- [] Issue a customized receipt (replica of the association receipt) to be downloaded with a QR code for the original
  payment confirmation

### President/Association Lead

- Signup/login to dashboard
    - [] Signup box: Full Name, Matriculation Number, School Name, School Short name, Association Name, Association
      shortened name,
      Level, Constituency name, Department or Faculty option, Session
- Add bank account details
    - [] Enter and verify account name compliance sake, changing it requires submission
    - [] Edition of account number requires checking for bank account number, is it matches that of the local bank and
      does
      the name matches the association name
- Add student's details submitted by students' class governors
    - [] The president/departmental president will see the start session button and select the session they are starting
    - [] The president gets the students' data from the departmental president populated for them
- [] Message/SMS option button to notify students who are yet to pay (proposed for v2)
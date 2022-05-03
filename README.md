# GNOSIS

## About
- GNOSIS is a Library Information System, built to automate commonly used services like Adding-Issuing-Reserving-Returing-Deleting Books, and managing Members and Clerks.
- The website is hosted on Heroku, check it out :
https://lis-gnosis.herokuapp.com/
## Software Pre-requisites
- Python 3 or above
- Django pre-installed
## Running the Tests
- Run `python3 manage.py test` on the terminal  in the `LIS` directory to run the Unit Tests given in the Test Plan.
- To run individual test files, run `python3 manage.py test tests.test_xyz`, where `xyz` is the name of the test file(without the `.py` extension).
## Running the Application
- To run the Software locally, the Librarian needs to add himself through the 'admin' page of Django as a one-time-process, after which he can create Library Clerks, Add Books, Add Members to the Library.
## Things to Know
- Run `python3 manage.py runserver` in the `LibInfoSys/LIS` directory to start running the app locally.
- Run `python3 manage.py createsuperuser` to create a superuser and login through the `/admin` page, to create the Librarian, once at start.
- Member unique IDs are of the form `XX_YYDDAAAAA` where XX represents UG or PG or RS or FAC depending on member type, YY is the year of registration and DD represents the department of the member, AAAAA standing for a unique code representing the member in the Institution.
- Clerk unique IDs are of the form `LIBC_AAAAAAAA`, where AAAAAAAA represents the unique representation of the clerk in the Library.
- Librarian unique ID can be set once at the start by the superuser.
## Basic Use Cases
- Member Registration.
- Member Login.
- Staff Login.
### Librarian
- Remove Members.
- Add/Remove Clerks.
- Check Issue Statistics of all Books.
- Send Reminders.
### Library Clerk
- Add Books.
- Delete those Books that are disposed by librarian.
- Process Return of Book by a Library Member.
### Library Member
- Issue Book
- Reserve Unavailable Book
- Return an Issued Book.
- Search Book in Library.
- View Reminders.
- View Issue History.

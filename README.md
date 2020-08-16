# SoA Wizards

## Backend
### Initialization
**Requirements:** Latest globally installed versions of: 
- python
- pip
- venv

cd into the cloned repository and issue the following commands (replace
*python3* with *python* for Windows): 
 
- Create the project's virtual environment with <code>python3 -m venv venv</code>
- Install the project's dependencies with <code>pip install -r requirements.txt</code>
- Make sure you **always** have the project's virtual environment activated when you're working with the project by 
issuing <code>source venv/bin/activate</code> (<code>venv/bin/activate.bat</code> for windows). Your shell's
commands should now be prefixed by *(venv)*).
- Generate the SQLite database by running the migrations with <code>python manage.py migrate</code>
- To check if it worked, run <code>python manage.py runserver</code> and navigate to the showed URL with */admin*
appended, you should see a login form. 

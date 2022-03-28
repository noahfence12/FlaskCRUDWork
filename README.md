# FlaskCRUDWork
To make sure this works correctly, please install sql-alchemy using:

pip3 install --user flask sqlalchemy flask-sqlalchemy

To build the database, type this into the command line:

python
from manager import db
db.create_all()
exit()

This should be created now. In order to run the app, type:
python manager.py

From here, you can add your information for the user.

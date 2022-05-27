# SQL_Alchemy Boiler Plate

## Requirements
```bash
pip3 install -r requirements.txt
```

## To Run
Create db in Flask shell
```bash
flask shell
db.create_all()
```
You should see 'data.db' show up in your file manager

Run in debug mode
```bash
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

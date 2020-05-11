import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


MONGODB_URI = os.environ.get("MONGO_URIL")
app.config["MONGO_DBNAME"] = 'golfDictionary'
app.config["MONGO_URI"] = MONGODB_URI

mongo = PyMongo(app)



@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/definitions')
def definitions_list():
    return render_template("definitions.html", definitions=mongo.db.entries.find())


@app.route('/definitions/<name>')
def definition(name):
    definition = {}
    definitions = mongo.db.entries.find()
    for obj in definitions:
        if obj["name"] == name:
            definition = obj
    return render_template("def.html", definition=definition)


@app.route('/add_definition')
def add_definition():
    return render_template('adddefinition.html', pageTitle='Add Definition', defi={})


@app.route('/insert_def', methods=['POST'])
def insert_def():
    entries = mongo.db.entries
    entries.insert_one(request.form.to_dict())
    return redirect(url_for('definitions_list'))


@app.route('/edit_def/<def_id>')
def edit_def(def_id):
    the_def = mongo.db.entries.find_one({"_id": ObjectId(def_id)})
    return render_template('editdef.html', defi=the_def)


@app.route('/update_def/<def_id>', methods=['POST'])
def update_def(def_id):
    defs = mongo.db.entries
    defs.update({'_id': ObjectId(def_id)},
    {
        'name': request.form.get('name'),
        'definition': request.form.get('definition'),
        'type': request.form.get('type')
    })
    return redirect(url_for('definitions_list'))


@app.route('/delete_def/<def_id>')
def delete_def(def_id):
    mongo.db.entries.remove({'_id': ObjectId(def_id)})
    return redirect(url_for('definitions_list'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
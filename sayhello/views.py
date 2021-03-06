# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import flash, redirect, url_for, render_template

from sayhello import app, db
from sayhello.forms import HelloForm, RestoreForm
from sayhello.models import Message

# This is AI algorithm
from sayhello.fact_entity_extraction import UserPredict

#
utils = UserPredict()
#


@app.route('/', methods=['GET', 'POST'])
def index():

    fact_form = HelloForm()

    if fact_form.validate_on_submit():
        # name = form.name.data
        body = fact_form.body.data
        c_type = fact_form.c_type.data

        nl_body = body

        # Handle if user input facts
        if c_type == "Facts":
            query_result = utils.query(body)

            if query_result:
                atom_clau = query_result[1]
                # print(atom_clause)
                body = str(atom_clau)
                entity = str(query_result[2])
            else:
                entity = None
                c_type = "Emotional"

        message = Message(body=body, c_type=c_type, nl_body=nl_body, entity=entity)
        db.session.add(message)
        db.session.commit()

        flash('Published 1 comment.')
        return redirect(url_for('index'))

    # Clear the database:
    restore_form = RestoreForm()
    if restore_form.validate_on_submit():
        if restore_form.password.data == "1234":
            pass

    messages = Message.query.order_by(Message.timestamp.desc()).all()

    # print(messages)

    facts = []
    predicates = []
    emotionals = []
    for i in messages:
        if i.c_type == "Facts":
            facts.append(i)
        elif i.c_type == "Predicates":
            predicates.append(i)
        elif i.c_type == "Emotional":
            emotionals.append(i)

    # for i in

    return render_template('index.html', fact_form=fact_form, restore_form=restore_form, predicates=predicates, facts=facts, emotionals=emotionals)

from flask import session, request, Blueprint, render_template, url_for, redirect, jsonify
import json

from tools.database_tools import DatabaseConnection


class FormsViews:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_tools = DatabaseConnection()

        self.forms_bp = Blueprint('forms', __name__, template_folder='templates')

        self.first_page()
        self.get_forms()

    def first_page(self):
        @self.forms_bp.route('/')
        def get_user():
            return render_template('get-user.html')

    def get_forms(self):
        @self.forms_bp.route('/formulaire-page/<int:num>', methods=['GET'])
        def get_form(num):
            if 'matricule' in session and session['matricule'] is not None:
                if int(session['page']) == int(num) or int(session['page']) < int(num):
                    if 'reponses' in session:
                        page_reponse = session['reponses'][str(num)]
                    else:
                        page_reponse = None
                    print(page_reponse)
                    return render_template(f'{num}.html', data=page_reponse, page=num)
            return redirect(url_for('forms.get_user'))

        @self.forms_bp.route('/post-responses', methods=['POST'])
        def post_responses():
            if session['matricule'] is not None:
                data = request.get_json()
                page = data.get('page')
                reponses = data.get('reponses')

                if 'reponses' not in session:
                    sr = {
                        '1': None,
                        '2': None,
                        '3': None,
                        '4': None,
                        '5': None,
                    }
                else:
                    sr = session['reponses']
                sr[str(page)] = reponses
                session['reponses'] = sr
                return jsonify({'status': 'success', 'load': 'success'})
            return jsonify({'status': 'failed', 'exist': 'false'})

        @self.forms_bp.route('/envoyer', methods=['GET'])
        def envoyer():
            if 'matricule' in session and session['matricule'] is not None and 'reponses' in session:
                rs = session['reponses']
                mat = session['matricule']
                email = session['email']
                if email is None:
                    email = ''
                type = session['type']
                if mat is None or type is None or rs is None:
                    return redirect(url_for('forms.get_user'))
                con, cursor = self.connection_tools.find_connection()
                cursor.execute(f"SELECT * FROM personne WHERE Matricule = '{mat}'")
                personne = cursor.fetchone()
                if not personne:
                    return jsonify({'status': 'failed', 'exist': 'false'})
                cursor.execute(f"SELECT * FROM reponse WHERE Matricule = '{mat}'")
                reponses = cursor.fetchall()
                if reponses:
                    return jsonify({'status': 'failed', 'exist': 'true', 'reponses': 'true'})
                nc, f = not_complete(rs)
                if nc:
                    return redirect(url_for('forms.get_form', num=f))
                try:
                    rewrite_response(mat, email, type, rs)
                except:
                    return jsonify({'status': 'failed', 'reason': 'UNKNOWN'})
                session.clear()
                return render_template('GB.html')
            else:
                return redirect(url_for('forms.get_user'))

        @self.forms_bp.route('/get-responses', methods=['GET'])
        def get_responses():
            if session['matricule'] is not None:
                print(session)
                return jsonify({'status': 'success', 'reponses': session, 'page': session['page']})

        @self.forms_bp.route('/delete-responses', methods=['GET'])
        def del_responses():
            session.clear()
            return jsonify({'status': 'success'})

        def rewrite_response(mat, mail, type, data):
            new_data_dict = generate_dict_for_json(data)
            json_data = convert_to_json(new_data_dict)
            print(json_data)
            con, cursor = self.connection_tools.find_connection()
            cursor.execute(
                "INSERT INTO reponse (Matricule, Mail, `Type`, Reponses) VALUES ('{}', '{}', '{}', '{}')".format(mat,
                                                                                                                 mail,
                                                                                                                 type,
                                                                                                                 json_data))
            con.commit()
            cursor.close()
            con.close()

        def generate_dict_for_json(data):
            new_dict = {}

            for form, questions in data.items():
                form_key = f"Form{form}"
                new_dict[form_key] = {}

                for q, ans in questions.items():
                    question_number = q.split('-')[1]
                    question_key = f"Q{question_number}"
                    answer_value = f"A{ans.split('-')[1][-1]}"
                    new_dict[form_key][question_key] = answer_value

            return new_dict

        def convert_to_json(data):
            return json.dumps(data, indent=4)

        def not_complete(data):
            for form, questions in data.items():
                if  questions is None:
                    return True, form
                for q, ans in questions.items():
                    if ans is None:
                        return True, form
            return False, -1


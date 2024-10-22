from flask import Blueprint, jsonify, session, request

from entities.personne import Personne
from tools.database_tools import DatabaseConnection


class PersonneView:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_tools = DatabaseConnection()

        self.personne_bp = Blueprint('personne', __name__, template_folder='templates')

        self.personne_routes()

    def personne_routes(self):
        @self.personne_bp.route('/existe', methods=['GET'])
        def exist():
            matricule = request.args.get('matricule')
            email = request.args.get('email')
            type = request.args.get('type')
            print(matricule)
            print(email)
            print(type)
            personne = Personne(matricule, "", "")
            conn, cursor = self.connection_tools.find_connection()
            cursor.execute(personne.find())
            result = cursor.fetchall()
            if result:
                cursor.execute(personne.have_answers())
                answers = cursor.fetchall()
                if answers:
                    conn.close()
                    return jsonify({'status': 'success', 'exist': 'true', 'answers': 'true'})
                else:
                    conn.close()
                    session['matricule'] = matricule
                    session['email'] = email
                    session['type'] = type
                    session['page'] = 1
                    return jsonify({'status': 'success','exist': 'true', 'answers': 'false'})
            conn.close()
            return jsonify({'status': 'success','exist': 'false', 'answers': 'false'})

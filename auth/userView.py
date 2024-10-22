from flask import session, request, Blueprint, render_template, url_for, redirect, jsonify
import json

from tools.database_tools import DatabaseConnection


class UserView:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_tools = DatabaseConnection()
        self.users = [
            {
                'username': 'fatma-zayani',
                'password': 'fatma-zayani-tesca',
                'role': 'admin'
            },
            {
                'username': '1',
                'password': '1',
                'role': 'user'
            }
        ]

        self.user_bp = Blueprint('user', __name__, template_folder='templates')
        self.user_routes()

    def user_routes(self):
        @self.user_bp.route('/')
        def get_user():
            return render_template('signup.html')

        @self.user_bp.route('/login-action', methods=['GET'])
        def login():
            username = request.args.get('username')
            password = request.args.get('password')
            if username and password:
                for user in self.users:
                    if user['username'] == username and user['password'] == password:
                        session['username'] = username
                        session['role'] = user['role']
                        return jsonify({'status': 'success', 'login': 'success'})
                if 'lgt' in session:
                    session['lgt'] += 1
                else:
                    session['lgt'] = 1
            return jsonify({'status': 'failed', 'login': 'failed'})

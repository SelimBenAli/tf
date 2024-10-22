from flask import session, request, Blueprint, render_template, url_for, redirect, jsonify
import json

from tools.database_tools import DatabaseConnection


class DashboardView:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connection_tools = DatabaseConnection()

        self.dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
        self.dashboard_routes()

    def dashboard_routes(self):
        @self.dashboard_bp.route('/')
        def open_dashboard():
            if 'username' in session and session['username'] is not None:
                con, cur = self.connection_tools.find_connection()
                cur.execute('SELECT COUNT(Matricule) FROM reponse')
                count_totale = cur.fetchone()
                cur.execute('SELECT COUNT(Matricule) FROM reponse WHERE `Type`="MOI"')
                count_moi = cur.fetchone()
                cur.execute('SELECT COUNT(Matricule) FROM reponse WHERE `Type`="MOD"')
                count_mod = cur.fetchone()
                cur.execute('SELECT COUNT(Matricule) FROM reponse WHERE `Type`="MOS"')
                count_mos = cur.fetchone()
                cur.execute('SELECT DISTINCT Service FROM personne')
                services = cur.fetchall()
                types = ['MOI', 'MOD', 'MOS']
                totales = [{'totale': count_moi[0]}, {'totale': count_mod[0]}, {'totale': count_mos[0]}]
                for type in types:
                    for service in services:
                        cur.execute(
                            f'SELECT COUNT(P.Matricule) FROM personne P, reponse R WHERE P.Service="{service[0]}" AND R.`Type`="{type}" AND P.Matricule = R.Matricule')
                        count_service = cur.fetchone()

                cur.execute('SELECT Reponses FROM reponse')
                reponses = cur.fetchall()
                reponses = [json.loads(reponse[0]) for reponse in reponses]
                print(reponses)
                dict_reponses = pourcentage_reponses(reponses)
                print(dict_reponses)
                cur.execute('SELECT COUNT(Matricule) FROM personne')
                count_personne = cur.fetchone()
                return render_template('dash.html', avg_moi=count_pourcentage(count_moi[0], count_totale[0]),
                                       avg_mod=count_pourcentage(count_mod[0], count_totale[0]),
                                       avg_mos=count_pourcentage(count_mos[0], count_totale[0]),
                                       avg_totale=count_pourcentage(count_totale[0], count_personne[0]),
                                       totale_reponses=count_totale[0],
                                       count_personne=count_personne[0], reponses=dict_reponses)
            return redirect(url_for('user.get_user'))

        def count_pourcentage(n, t):
            try:
                return round((n / t) * 100, 2)
            except:
                return 0

        def pourcentage_reponses(liste_reponses):
            dict_reponses = {'Form1': {'Q1': {'1': 0, '2': 0, '3': 0, '4': 0},
                                       'Q2': {'1': 0, '2': 0, '3': 0},
                                       'Q3': {'1': 0, '2': 0, '3': 0},
                                       'Q4': {'1': 0, '2': 0, '3': 0},
                                       'Q5': {'1': 0, '2': 0, '3': 0},
                                       'Q6': {'1': 0, '2': 0, '3': 0}},

                             'Form2': {'Q1': {'1': 0, '2': 0, '3': 0},
                                       'Q2': {'1': 0, '2': 0},
                                       'Q3': {'1': 0, '2': 0},
                                       'Q4': {'1': 0, '2': 0, '3': 0},
                                       'Q5': {'1': 0, '2': 0, '3': 0},
                                       'Q6': {'1': 0, '2': 0},
                                       'Q7': {'1': 0, '2': 0, '3': 0},
                                       'Q8': {'1': 0, '2': 0, '3': 0},
                                       },

                             'Form3': {'Q1': {'1': 0, '2': 0, '3': 0},
                                       'Q2': {'1': 0, '2': 0, '3': 0},
                                       'Q3': {'1': 0, '2': 0, '3': 0},
                                       'Q4': {'1': 0, '2': 0, '3': 0},
                                       'Q5': {'1': 0, '2': 0, '3': 0},
                                       'Q6': {'1': 0, '2': 0, '3': 0}},

                             'Form4': {'Q1': {'1': 0, '2': 0},
                                       'Q2': {'1': 0, '2': 0, '3': 0},
                                       'Q3': {'1': 0, '2': 0, '3': 0},
                                       'Q4': {'1': 0, '2': 0},
                                       'Q5': {'1': 0, '2': 0, '3': 0},
                                       'Q6': {'1': 0, '2': 0, '3': 0}},

                             'Form5': {'Q1': {'1': 0, '2': 0, '3': 0},
                                       'Q2': {'1': 0, '2': 0, '3': 0},
                                       'Q3': {'1': 0, '2': 0, '3': 0},
                                       'Q4': {'1': 0, '2': 0, '3': 0},
                                       'Q5': {'1': 0, '2': 0, '3': 0},
                                       'Q6': {'1': 0, '2': 0, '3': 0}},

                             }

            for reponses in liste_reponses:
                for form in reponses:
                    for question in reponses[form]:
                        print(form, question, reponses[form][question])
                        dict_reponses[form][question][reponses[form][question][1]] += 1

            return dict_reponses

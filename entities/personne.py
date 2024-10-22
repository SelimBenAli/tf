class Personne:
    def __init__(self, mat, nom, service):
        self.matricule = mat
        self.nom = nom
        self.service = service

    def __str__(self):
        return f"{self.matricule} - {self.nom} - {self.service}"

    def convert(self):
        return {
            'matricule': self.matricule,
            'nom': self.nom,
            'service': self.service
        }

    def reduce_convert(self):
        return {
            'matricule': self.matricule,
            'nom': self.nom
        }

    def find(self):
        return "SELECT * FROM personne WHERE Matricule = '{}'".format(self.matricule)

    def have_answers(self):
        return "SELECT * FROM reponse WHERE Matricule = '{}'".format(self.matricule)

from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'sandbox94769d8d532747ada290b60f4bf892d5.mailgun.org'
MAILGUN_API_KEY = '83871d96f0097a0955e85370b80fabde-6e0fd3a4-47abbf00'
FROM_TITLE = 'NO REPLY'
FROM_EMAIL = 'no-reply@rest-api.com.br'

class UserModel(banco.Model):
    __tablename__ = 'users'
    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = banco.Column(banco.String(80), nullable=False)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    password = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    activate = banco.Column(banco.Boolean, default=False)

    def __init__(self, name, login, password, email, activate):
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.activate = activate

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'login': self.login,
            'email': self.email,
            'activate': self.activate
        }
    
    def email_confirm(self):
        link = request.url_root[:-1] + url_for('useractivate', id=self.id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                                                            auth=('api', MAILGUN_API_KEY),
                                                            data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                                                                    'to': self.email,
                                                                    'subject': 'Confirmação de cadastro',
                                                                    'text': 'Confirme seu cadastro clicando no link: {}'.format(link),
                                                                    'html': '<html><p>\
                                                                        Confirme seu cadastro clicando no link: <a href="{}">CONFIRMAR E-MAIL</a>\
                                                                        </p></html>'.format(link)
                                                                }
                    )

    @classmethod
    def user_find(cls,id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def user_save(self):
        banco.session.add(self)
        banco.session.commit()
    
    def user_delete(self):
        banco.session.delete(self)
        banco.session.commit()
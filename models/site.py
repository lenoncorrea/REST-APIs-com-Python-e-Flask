from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'
    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    name = banco.Column(banco.String(80), nullable=False)
    url = banco.Column(banco.String(80), nullable=False)
    hotels = banco.relationship('HotelModel')

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'hotels': [hotel.json() for hotel in self.hotels]
        }

    @classmethod
    def find_site_by_id(cls, id):
        site = cls.query.filter_by(id=id).first()
        if site:
            return site
        return None

    @classmethod
    def find_site_by_name(cls, name):
        site = cls.query.filter_by(name=name).first()
        if site:
            return site
        return None

    @classmethod
    def find_site_by_url(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hotels]
        banco.session.delete(self)
        banco.session.commit()
from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hotels'
    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    name = banco.Column(banco.String(80))
    stars = banco.Column(banco.Float(precision=1))
    daily = banco.Column(banco.Float(precision=2))
    state = banco.Column(banco.String(80))
    city = banco.Column(banco.String(80))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.id'))

    def __init__(self, name, stars, daily, state, city, site_id):
        self.name = name
        self.stars = stars
        self.daily = daily
        self.state = state
        self.city = city
        self.site_id = site_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'stars': self.stars,
            'daily': self.daily,
            'state': self.state,
            'city': self.city,
            'site_id': self.site_id
        }
    
    @classmethod
    def hotel_find_by_name(cls, name):
        hotel = cls.query.filter_by(name=name).first()
        if hotel:
            return hotel
        return None

    @classmethod
    def hotel_find_by_id(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()
    
    def update_hotel(self, name, stars, daily, state, city, site_id):
        self.name = name
        self.stars = stars
        self.daily = daily
        self.state = state
        self.city = city
        self.site_id = site_id

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
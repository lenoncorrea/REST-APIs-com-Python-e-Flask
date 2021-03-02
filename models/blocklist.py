from sql_alchemy import banco

class BlocklistModel(banco.Model):
    __tablename__ = 'blocklist'
    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    jti = banco.Column(banco.String(36), nullable=False)
    created_at = banco.Column(banco.DateTime, nullable=False)

    def blocklist_add(jti, now):
        banco.session.add(BlocklistModel(jti=jti, created_at=now))
        banco.session.commit()
        return True
    
    @classmethod
    def token_filter(cls, jti):
        token = banco.session.query(cls.id).filter_by(jti=jti).scalar()
        return token
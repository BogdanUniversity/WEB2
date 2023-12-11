from app import db


class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(500))


class FollowingTable(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    UserID = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    FolloweeID = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)

    # Defines a relationship
    user = db.relationship('UserTable', foreign_keys=[UserID])
    folowee = db.relationship('UserTable', foreign_keys=[FolloweeID])


class PostTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    like_count = db.Column(db.Integer, default = 0 )

    # Defines a relationship back to the UserTable
    user = db.relationship('UserTable', foreign_keys=[user_id])


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post_table.id'), nullable = False)

    user = db.relationship('UserTable', foreign_keys=[user_id])
    post = db.relationship('PostTable',foreign_keys=[post_id])

"""



class Incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income_name = db.Column(db.String(500))
    income_type = db.Column(db.String(500))
    transaction_date = db.Column(db.DateTime)
    income_amount = db.Column(db.Float)


class Expences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expence_name = db.Column(db.String(500))
    expence_type = db.Column(db.String(500))
    transaction_date = db.Column(db.DateTime)
    expence_amount = db.Column(db.Float)


class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(500))
    goal_amount = db.Column(db.Float)
"""
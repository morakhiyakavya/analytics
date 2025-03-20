# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func

# db = SQLAlchemy()

# # UserDetails Model
# class UserDetails(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ip_address = db.Column(db.String(40), nullable=True)
#     city = db.Column(db.String(100), nullable=True)
#     region = db.Column(db.String(100), nullable=True)
#     country = db.Column(db.String(100), nullable=True)

#     # One-to-one relationship with User model
#     user = db.relationship('User', back_populates='details', uselist=False, passive_deletes=True)

#     def __repr__(self):
#         return f'<UserDetails {self.city}, {self.region}, {self.country}>'

# # User Model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime, default=func.now())
#     updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

#     details = db.relationship('UserDetails', back_populates='user', uselist=False)
#     feedback = db.relationship('UserFeedback', back_populates='user', passive_deletes=True)
#     behavior = db.relationship('UserBehaviour', back_populates='user', passive_deletes=True)
#     web_traffic = db.relationship('WebTraffic', back_populates='user', passive_deletes=True)


# # User Behaviour Model
# class UserBehaviour(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
#     session_id = db.Column(db.String(100), nullable=True, index=True)  # Tracking guests
#     login_count = db.Column(db.Integer, default=0)
#     last_login = db.Column(db.DateTime, nullable=True)
#     page_visits = db.Column(db.Integer, default=0)
#     last_page_visit = db.Column(db.DateTime, nullable=True)
#     session_duration = db.Column(db.Integer, nullable=True)  # Store in seconds
#     actions = db.Column(db.JSON, nullable=True)
#     device = db.Column(db.String(100), nullable=True)
#     browser = db.Column(db.String(100), nullable=True)
#     os = db.Column(db.String(100), nullable=True)

#     user = db.relationship('User', back_populates='behavior')


# # User Feedback Model
# class User_Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     feedback = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     feedback_type = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=func.now())
#     updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

#     user = db.relationship('User', back_populates='feedback')

#     def __repr__(self):
#         return f'<User_Feedback {self.id}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()
    
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @staticmethod
#     def get_all():
#         return User_Feedback.query.all()

# # Web Traffic Model
# class WebTraffic(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
#     session_id = db.Column(db.String(100), nullable=True, index=True)  # Allow guest tracking
#     traffic_source = db.Column(db.String(100), nullable=False)
#     page_views = db.Column(db.Integer, default=0)
#     device_type = db.Column(db.String(100), nullable=False)
#     browser = db.Column(db.String(100), nullable=False)
#     session_duration = db.Column(db.Integer, nullable=True)  # Store as seconds
#     unique_visitors = db.Column(db.Integer, default=0)
#     created_at = db.Column(db.DateTime, default=func.now())
#     updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

#     user = db.relationship('User', back_populates='web_traffic')

# # Conversion Funnel Model
# class ConversionFunnel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
#     session_id = db.Column(db.String(100), nullable=True, index=True)  # Track guest users
#     funnel_id = db.Column(db.String(100), nullable=False)
#     step_name = db.Column(db.String(100), nullable=False)
#     step_timestamp = db.Column(db.DateTime, default=func.now())
#     step_completed = db.Column(db.Boolean, default=False)


# # Social Media Engagement Model
# class SocialMediaEngagement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
#     session_id = db.Column(db.String(100), nullable=True, index=True)  # Allow guest tracking
#     engagement_id = db.Column(db.String(100), nullable=False)
#     platform = db.Column(db.String(100), nullable=False)
#     engagement_type = db.Column(db.String(100), nullable=False)
#     engagement_timestamp = db.Column(db.DateTime, default=func.now())
#     content = db.Column(db.Text, nullable=True)


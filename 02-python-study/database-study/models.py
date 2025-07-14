from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

#create SQLAlchemy instance
db = SQLAlchemy()

class Todo(db.Model):
    """
    TODO Model - database table mapping
    similar to JAVA JAP Entity
    """
    #set table nm
    __tablename__ = 'todos'

    #set colums
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #pk
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        """Define object output format (similar to Java's toString())"""
        return f'<Todo {self.id} {self.title}>'

    def to_dict(self):
        """Convert object to dictionary (for JSON response)"""
        return {
            'id' : self.id,
            'title' : self.title,
            'completed' : self.completed,
            'created_at' : self.created_at.isoformat(),
            'updated_at' : self.updated_at.isoformat()
        }
    # Java JPA:
    # @Entity
    # public class Todo {
    #     @Id @GeneratedValue
    #     private Long id;
    #
    #     @Column(nullable = false)
    #     private String title;
    #
    #     @Column(nullable = false)
    #     private Boolean completed = false;
    # }
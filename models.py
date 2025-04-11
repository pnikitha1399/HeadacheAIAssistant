from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HeadacheRecord(db.Model):
    """Model to store user headache symptoms and AI analysis results"""
    id = db.Column(db.Integer, primary_key=True)
    
    # User input
    symptoms = db.Column(db.Text, nullable=False)
    
    # Analysis results
    diagnosis = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=False)  # Stored as JSON string
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_fallback = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<HeadacheRecord id={self.id} created_at={self.created_at}>"
import os

class Config:
    SQLALCHEMY_DATABASE_URI =os.getenv('DATABASE_URL') or 'mysql+pymysql://user:test@db/qc_automation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class Config:

    # SQLite Database Connection (easier setup)
    SQLALCHEMY_DATABASE_URI = "sqlite:///expense_tracker.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "expense_tracker_secret_key"
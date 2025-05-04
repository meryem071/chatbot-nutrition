from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Config
from models import Base, User, Conversation, Message
from datetime import datetime

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def save_user(email, password, extra_data=None):
    session = SessionLocal()
    try:
        user = User(email=email, password=password)
        
        # Si extra_data contient des infos supplémentaires (ex: prénom, âge)
        if extra_data:
            for key, value in extra_data.items():
                setattr(user, key, value)

        session.add(user)
        session.commit()
    finally:
        session.close()

def verify_duplicate_user(email):
    session = SessionLocal()
    exists = session.query(User).filter_by(email=email).first() is not None
    session.close()
    return exists

def authenticate_user(email, password):
    session = SessionLocal()
    user = session.query(User).filter_by(email=email, password=password).first()
    session.close()
    return user is not None


def create_conversation(user_email, title="Nouvelle conversation"):
    session = SessionLocal()
    user = session.query(User).filter_by(email=user_email).first()
    if not user:
        session.close()
        return None
    conversation = Conversation(user_id=user.id, title=title)
    session.add(conversation)
    session.commit()
    conv_id = conversation.id
    session.close()
    return conv_id


def save_message(conversation_id, role, content):
    session = SessionLocal()
    message = Message(conversation_id=conversation_id, role=role, content=content)
    session.add(message)
    session.commit()
    session.close()


def get_user_conversations(email):
    session = SessionLocal()
    user = session.query(User).filter_by(email=email).first()
    if not user:
        session.close()
        return []
    conversations = user.conversations
    session.close()
    return conversations


def get_user_conversations(email):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return []

        conversations = (
            session.query(Conversation)
            .filter_by(user_id=user.id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

        # Charger les messages associés pour chaque conversation
        for conv in conversations:
            conv.messages = (
                session.query(Message)
                .filter_by(conversation_id=conv.id)
                .order_by(Message.timestamp.asc())
                .all()
            )

        return conversations
    finally:
        session.close()



def get_conversation_messages(conversation_id):
    session = SessionLocal()
    messages = session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
    session.close()
    return messages

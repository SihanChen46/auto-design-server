from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"
    conversation_id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    created_timestamp = Column(DateTime, nullable=False)


class Message(Base):
    __tablename__ = "messages"
    msg_id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), nullable=False)
    user_id = Column(String(36))
    creator_role = String(10, nullable=False)
    msg_content = Column(String(255), nullable=False)
    created_timestamp = Column(DateTime, nullable=False)


class Design(Base):
    __tablename__ = "designs"
    design_id = Column(String(36), primary_key=True)
    conversation_id = conversation_id = Column(String(36), nullable=False)
    user_id = Column(String(36))
    design_content = Column(String(255), nullable=False)
    created_timestamp = Column(DateTime, nullable=False)


class Understanding(Base):
    __tablename__ = "understandings"
    understanding_id = Column(String(36), primary_key=True)
    conversation_id = conversation_id = Column(String(36), nullable=False)
    user_id = Column(String(36))
    understanding_content = Column(String(255), nullable=False)
    created_timestamp = Column(DateTime, nullable=False)


class Diagram(Base):
    __tablename__ = "diagrams"
    diagram_id = Column(String(36), primary_key=True)
    conversation_id = conversation_id = Column(String(36), nullable=False)
    user_id = Column(String(36))
    diagram_content = Column(String(255), nullable=False)
    created_timestamp = Column(DateTime, nullable=False)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import JobRequirement, Resume, Interview, User

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Import all models to ensure they're registered with Base
    from app.models import Base, JobRequirement, Resume, Interview, User
    # Drop all tables to ensure clean state
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test session to verify tables are created
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    test_session = TestingSessionLocal()
    try:
        # Try to create a test user to verify database setup
        test_user = User(
            username="test_setup",
            email="test@example.com",
            password_hash="test",
            role="admin"
        )
        test_session.add(test_user)
        test_session.commit()
        test_session.refresh(test_user)
    finally:
        test_session.close()
    
    return engine

@pytest.fixture
def test_user(db_session):
    user = User(
        username="test_interviewer",
        email="interviewer@test.com",
        password_hash="hashed_password",
        role="interviewer"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def db_session(test_db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

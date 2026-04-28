import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from myapp.app import create_app
from myapp.app.db import get_db, teardown_db
from myapp.app.models import User
from myapp.config import TestingConfig


def test_get_db_creates_engine_from_app_config(app):
    app.config.update(
        DB_USER="user",
        DB_PASSWORD="pwd",
        DB_HOST="localhost",
        DB_PORT="3306",
        DB_NAME="testdb",
    )

    with app.app_context():
        with patch("myapp.app.db.create_engine") as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            engine1 = get_db()
            engine2 = get_db()

            assert engine1 is engine2
            mock_create_engine.assert_called_once_with(
                "mysql+pymysql://user:pwd@localhost:3306/testdb"
            )


def test_teardown_db_disposes_engine(app):
    with app.app_context():
        mock_engine = MagicMock()
        from flask import g
        g._db_engine = mock_engine

        teardown_db(None)

        mock_engine.dispose.assert_called_once()
        assert not hasattr(g, "_db_engine")


def test_user_get_by_id_returns_user():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    row = SimpleNamespace(id=1, username="tester", email="test@example.com", password_hash="hashed")
    mock_conn.execute.return_value.fetchone.return_value = row

    user = User.get_by_id(mock_engine, 1)

    assert user is not None
    assert user.id == 1
    assert user.username == "tester"
    assert user.email == "test@example.com"


def test_user_get_by_email_returns_none_when_missing():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.fetchone.return_value = None

    user = User.get_by_email(mock_engine, "missing@example.com")

    assert user is None


def test_user_create_user_inserts_record_and_commits():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    with patch("myapp.app.models.generate_password_hash", return_value="fakehash") as mock_hash:
        User.create_user(mock_engine, "newuser", "New@Example.com", "secret")

    mock_hash.assert_called_once_with("secret")
    mock_conn.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    executed_text = mock_conn.execute.call_args.args[0]
    assert "INSERT INTO users" in str(executed_text)

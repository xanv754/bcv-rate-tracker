import pytest
from sqlalchemy import URL

from utils.env.database import DatabaseConfig
from utils.errors import DatabaseConfigError


class TestDatabaseConfigDefaults:
    def test_host_defaults_when_env_var_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DB_HOST", raising=False)

        assert DatabaseConfig.host() == "localhost"

    def test_host_uses_env_var_when_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_HOST", "db.internal")

        assert DatabaseConfig.host() == "db.internal"

    def test_port_defaults_when_env_var_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DB_PORT", raising=False)

        assert DatabaseConfig.port() == 5432

    def test_port_uses_env_var_when_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_PORT", "6543")

        assert DatabaseConfig.port() == 6543

    def test_sslmode_defaults_to_none_when_env_var_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("DB_SSLMODE", raising=False)

        assert DatabaseConfig.sslmode() is None

    def test_sslmode_uses_env_var_when_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_SSLMODE", "require")

        assert DatabaseConfig.sslmode() == "require"


class TestDatabaseConfigRequiredValues:
    @pytest.mark.parametrize(
        ("accessor", "env_var"),
        [
            (DatabaseConfig.name, "DB_NAME"),
            (DatabaseConfig.user, "DB_USER"),
            (DatabaseConfig.password, "DB_PASSWORD"),
        ],
    )
    def test_raises_when_required_env_var_missing(
        self, monkeypatch: pytest.MonkeyPatch, accessor, env_var: str
    ) -> None:
        monkeypatch.delenv(env_var, raising=False)

        with pytest.raises(DatabaseConfigError):
            accessor()

    def test_returns_value_when_env_var_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_NAME", "bcv_test_db")

        assert DatabaseConfig.name() == "bcv_test_db"


class TestDatabaseConfigUrl:
    def test_builds_expected_connection_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_HOST", "db.internal")
        monkeypatch.setenv("DB_PORT", "6543")
        monkeypatch.setenv("DB_NAME", "bcv_db")
        monkeypatch.setenv("DB_USER", "bcv_user")
        monkeypatch.setenv("DB_PASSWORD", "secret")
        monkeypatch.delenv("DB_SSLMODE", raising=False)

        url = DatabaseConfig.url()

        assert isinstance(url, URL)
        assert url.drivername == "postgresql+psycopg"
        assert url.host == "db.internal"
        assert url.port == 6543
        assert url.database == "bcv_db"
        assert url.username == "bcv_user"
        assert url.password == "secret"

    def test_builds_url_without_sslmode_query_param_when_not_set(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DB_HOST", "db.internal")
        monkeypatch.setenv("DB_PORT", "6543")
        monkeypatch.setenv("DB_NAME", "bcv_db")
        monkeypatch.setenv("DB_USER", "bcv_user")
        monkeypatch.setenv("DB_PASSWORD", "secret")
        monkeypatch.delenv("DB_SSLMODE", raising=False)

        url = DatabaseConfig.url()

        assert url.query == {}

    def test_builds_url_with_sslmode_query_param_when_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DB_HOST", "db.internal")
        monkeypatch.setenv("DB_PORT", "6543")
        monkeypatch.setenv("DB_NAME", "bcv_db")
        monkeypatch.setenv("DB_USER", "bcv_user")
        monkeypatch.setenv("DB_PASSWORD", "secret")
        monkeypatch.setenv("DB_SSLMODE", "require")

        url = DatabaseConfig.url()

        assert url.query == {"sslmode": "require"}

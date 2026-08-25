from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from storage.database import Database
from storage.models import ExchangeRate, ScrapeRun
from transform import BCVTransformer, TransformResult
from utils.errors import DatabaseConnectionError, DatabasePersistError


class BCVStorage:
    @staticmethod
    def execute(result: TransformResult) -> None:
        """Persist a scrape run and its exchange rates, skipping dates already stored."""
        session = Database().get_session()
        try:
            session.add(ScrapeRun(**result.scrape_run.model_dump()))

            for rate in result.rates:
                already_stored = session.execute(
                    select(ExchangeRate.id).where(
                        ExchangeRate.currency == rate.currency,
                        ExchangeRate.official_date == rate.official_date,
                    )
                ).scalar_one_or_none()
                if already_stored is None:
                    session.add(ExchangeRate(**rate.model_dump()))

            session.commit()
        except OperationalError as exc:
            session.rollback()
            raise DatabaseConnectionError(f"Could not connect to the database: {exc}") from exc
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabasePersistError(f"Failed to persist scrape result: {exc}") from exc
        finally:
            session.close()


if __name__ == "__main__":
    Database().create_tables()
    transform_result = BCVTransformer.execute()
    BCVStorage.execute(transform_result)
    print(transform_result)

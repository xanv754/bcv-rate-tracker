import click

from storage import BCVStorage, Database
from transform import BCVTransformer, ScrapeRunStatus
from utils.errors import AppError
from utils.outputs import ConsoleOutput


class BCVCli:
    """Command implementations backing the bcv-scraper CLI."""

    @staticmethod
    def init_db() -> None:
        """Create the exchange_rates and scrape_runs tables if they do not yet exist."""
        console = ConsoleOutput()
        with console.loading("Initializing database..."):
            Database().create_tables()
        console.success("Database is ready.")

    @staticmethod
    def run() -> None:
        """Scrape, validate and persist today's BCV exchange rates."""
        console = ConsoleOutput()
        with console.loading("Fetching BCV exchange rates..."):
            result = BCVTransformer.execute()
            BCVStorage.execute(result)

        if result.scrape_run.status == ScrapeRunStatus.FAILED:
            console.error(f"Run failed: {result.scrape_run.error_message}")
            raise SystemExit(1)

        console.success(f"Stored {len(result.rates)} exchange rate(s).")


@click.group()
def cli() -> None:
    """BCV Scraper command-line interface."""


@cli.command("init-db")
def init_db_command() -> None:
    """Create the database tables if they don't exist yet."""
    try:
        BCVCli.init_db()
    except AppError as error:
        ConsoleOutput().error(str(error))
        raise SystemExit(1) from error


@cli.command("run")
def run_command() -> None:
    """Fetch, validate and store today's BCV exchange rates."""
    try:
        BCVCli.run()
    except AppError as error:
        ConsoleOutput().error(str(error))
        raise SystemExit(1) from error


def main() -> None:
    cli()


if __name__ == "__main__":
    main()

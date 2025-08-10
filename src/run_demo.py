from __future__ import annotations

from rich import print as rprint  # optional; remove if you don't want rich formatting

from src.config import load_settings, make_client
from src.agent.core import Agent

def main() -> None:
    settings = load_settings()
    client = make_client(settings)
    agent = Agent(client, settings)

    rprint("[bold cyan]Phase 1: Propose a challenging question[/bold cyan]")
    q = agent.propose_question()
    rprint(f"[yellow]Question:[/yellow] {q}")

    rprint("\n[bold cyan]Phase 2: Solve with tools if needed[/bold cyan]")
    ans = agent.solve(q)
    rprint(f"[green]Answer:[/green] {ans}")

    rprint("\n[dim]Done.[/dim]")


if __name__ == "__main__":
    main()

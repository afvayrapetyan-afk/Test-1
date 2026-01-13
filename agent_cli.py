#!/usr/bin/env python3
"""
CLI для работы с AI агентами
Использование: python agent_cli.py [command] [args]

Примеры:
  python agent_cli.py analyze backend/main.py
  python agent_cli.py bugs backend/api/code.py
  python agent_cli.py implement "Add rate limiting"
  python agent_cli.py tests backend/services/github.py
"""
import asyncio
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agents import CodeAnalystAgent, DevAgent

console = Console()


async def cmd_analyze(file_path: str):
    """Анализ файла"""
    console.print(f"\n[bold blue]🔍 Analyzing {file_path}...[/bold blue]\n")

    agent = CodeAnalystAgent()
    result = await agent.analyze_file(file_path)

    analysis = result['analysis']

    # Scores table
    table = Table(title="📊 Scores")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", style="magenta")

    table.add_row("Quality", f"{analysis['quality_score']}/100")
    table.add_row("Readability", f"{analysis['readability_score']}/100")
    table.add_row("Maintainability", f"{analysis['maintainability_score']}/100")
    table.add_row("Performance", f"{analysis['performance_score']}/100")

    console.print(table)

    # Issues
    if analysis['issues']:
        console.print(f"\n[bold red]⚠️  Issues ({len(analysis['issues'])}):[/bold red]")
        for issue in analysis['issues'][:5]:
            console.print(f"  • [{issue['severity']}] {issue['description']}")


async def cmd_bugs(file_path: str):
    """Поиск багов"""
    console.print(f"\n[bold orange1]🐛 Finding bugs in {file_path}...[/bold orange1]\n")

    agent = CodeAnalystAgent()
    bugs = await agent.find_bugs(file_path)

    if not bugs:
        console.print("[green]✅ No bugs found![/green]")
        return

    console.print(f"[bold red]Found {len(bugs)} potential bugs:[/bold red]\n")

    for i, bug in enumerate(bugs[:10], 1):
        console.print(Panel(
            f"[{bug['severity']}] {bug['description']}\n\n"
            f"Line: {bug.get('line', 'N/A')}\n"
            f"Fix: {bug.get('fix', 'See recommendations')}",
            title=f"Bug #{i}",
            border_style="red"
        ))


async def cmd_security(file_path: str):
    """Security проверка"""
    console.print(f"\n[bold red]🔒 Security audit: {file_path}...[/bold red]\n")

    agent = CodeAnalystAgent()
    security = await agent.check_security(file_path)

    console.print(f"[bold]Security Score:[/bold] {security['security_score']}/100\n")

    if security['vulnerabilities']:
        console.print(f"[bold red]🚨 Vulnerabilities ({len(security['vulnerabilities'])}):[/bold red]")
        for vuln in security['vulnerabilities'][:5]:
            console.print(
                f"  • [{vuln['severity']}] {vuln['type']}\n"
                f"    {vuln['description']}\n"
            )
    else:
        console.print("[green]✅ No vulnerabilities found![/green]")


async def cmd_implement(description: str):
    """Реализовать фичу"""
    console.print(f"\n[bold purple]✨ Implementing: {description}...[/bold purple]\n")

    agent = DevAgent()
    result = await agent.implement_feature(description, create_pr=True)

    console.print(Panel(
        f"[bold green]✅ Feature implemented![/bold green]\n\n"
        f"Branch: {result['branch']}\n"
        f"Files modified: {result['files_modified']}\n"
        f"PR: {result['pr']['url'] if result.get('pr') else 'Not created'}",
        border_style="green"
    ))


async def cmd_tests(file_path: str):
    """Генерация тестов"""
    console.print(f"\n[bold green]🧪 Generating tests for {file_path}...[/bold green]\n")

    agent = DevAgent()
    result = await agent.generate_tests(file_path)

    console.print(Panel(
        f"[bold green]✅ Tests generated![/bold green]\n\n"
        f"Test file: {result['test_file']}\n"
        f"Framework: {result['framework']}\n"
        f"Coverage: {result['estimated_coverage']}",
        border_style="green"
    ))


async def cmd_status():
    """Проверить статус агентов"""
    console.print("\n[bold cyan]🤖 Checking agents status...[/bold cyan]\n")

    import requests

    try:
        response = requests.get("http://localhost:8000/api/agents/status")
        data = response.json()

        table = Table(title="Agent Status")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Model", style="yellow")

        for agent in data['agents']:
            status = "🟢 Active" if agent['status'] == 'active' else "🔴 Inactive"
            table.add_row(agent['name'], status, agent['model'])

        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ Backend not running: {e}[/red]")


def print_help():
    """Показать помощь"""
    rprint("\n[bold cyan]🤖 AI Agents CLI[/bold cyan]\n")
    rprint("[bold]Commands:[/bold]")
    rprint("  [cyan]analyze[/cyan] <file>        - Analyze code quality")
    rprint("  [cyan]bugs[/cyan] <file>           - Find potential bugs")
    rprint("  [cyan]security[/cyan] <file>       - Security audit")
    rprint("  [cyan]implement[/cyan] <desc>      - Implement feature")
    rprint("  [cyan]tests[/cyan] <file>          - Generate tests")
    rprint("  [cyan]status[/cyan]               - Check agent status")
    rprint("\n[bold]Examples:[/bold]")
    rprint('  python agent_cli.py analyze backend/main.py')
    rprint('  python agent_cli.py implement "Add rate limiting"')
    rprint("")


async def main():
    """Main CLI handler"""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    try:
        if command == 'analyze':
            await cmd_analyze(sys.argv[2])
        elif command == 'bugs':
            await cmd_bugs(sys.argv[2])
        elif command == 'security':
            await cmd_security(sys.argv[2])
        elif command == 'implement':
            await cmd_implement(' '.join(sys.argv[2:]))
        elif command == 'tests':
            await cmd_tests(sys.argv[2])
        elif command == 'status':
            await cmd_status()
        elif command in ['help', '-h', '--help']:
            print_help()
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            print_help()

    except IndexError:
        console.print("[red]Missing arguments![/red]")
        print_help()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Load .env
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

    asyncio.run(main())

"""
Simple CLI tool for Resume Analyzer API
"""
import asyncio
import json
import subprocess
import time
import sys

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def start_server():
    """Start the FastAPI server in the background"""
    console.print("[cyan]Starting FastAPI server...[/cyan]")
    
    # Start server without capturing output so logs show in terminal
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
    )
    
    # Wait for server to start
    console.print("[yellow]Waiting for server to be ready...[/yellow]")
    time.sleep(3)  # Give it a few seconds to start
    
    return process


async def check_server_health():
    """Check if server is running"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            return response.status_code == 200
    except:
        return False


async def analyze_resume():
    """Send analysis request to the API"""
    # Load payload from payload.json
    console.print("\n[cyan]Loading payload from payload.json...[/cyan]")
    with open('data/payload.json', 'r', encoding='utf-8') as f:
        payload = json.load(f)
    
    # Send request
    console.print("[yellow]Sending request to API...[/yellow]\n")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing resume...", total=None)
            
            response = await client.post(
                "http://localhost:8000/api/v1/resume-analyzer/analyze",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            progress.update(task, completed=True)
    
    # Display results
    console.print("\n[green]✓ Analysis Complete![/green]\n")
    console.print(json.dumps(result, indent=2))
    
    # Save to results.json
    with open('data/results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    console.print("\n[green]Results saved to results.json[/green]")


async def main():
    """Main function"""
    server_process = None
    
    try:
        # Check if server is already running
        is_running = await check_server_health()
        
        if not is_running:
            # Start the server
            server_process = start_server()
            
            # Wait and verify server is ready
            max_retries = 10
            for i in range(max_retries):
                if await check_server_health():
                    console.print("[green]✓ Server is ready![/green]")
                    break
                if i < max_retries - 1:
                    console.print(f"[yellow]Waiting for server... ({i+1}/{max_retries})[/yellow]")
                    time.sleep(2)
            else:
                console.print("[red]Error: Server failed to start[/red]")
                return
        else:
            console.print("[green]✓ Server is already running![/green]\n")
        
        # Run the analysis
        await analyze_resume()
        
    except FileNotFoundError:
        console.print("[red]Error: payload.json not found![/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        # Clean up server if we started it
        if server_process:
            console.print("\n[yellow]Shutting down server...[/yellow]")
            server_process.terminate()
            server_process.wait()
            console.print("[green]✓ Server stopped[/green]")


if __name__ == "__main__":
    asyncio.run(main())
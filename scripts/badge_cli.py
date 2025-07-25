#!/usr/bin/env python3
"""
GitHub Achievement CLI

Master CLI tool for earning GitHub achievement badges.
"""

import os
import sys
import click
from colorama import init, Fore, Style

init(autoreset=True)

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🏆 GitHub Achievement Badge Automation CLI
    
    Master tool for earning GitHub achievement badges efficiently.
    Use this CLI to access all automation tools and guides.
    """
    pass

@cli.command()
def status():
    """Check your current badge progress"""
    click.echo(f"{Fore.CYAN}Checking badge progress...")
    os.system(f"python {os.path.dirname(__file__)}/badge_tracker.py summary")

@cli.command()
@click.option('--language', help='Filter by programming language')
@click.option('--interactive', is_flag=True, help='Interactive mode')
def find_repos(language, interactive):
    """Find repositories for contributions (Heart On Your Sleeve, Pull Shark)"""
    cmd = f"python {os.path.dirname(__file__)}/pr_automation.py"
    if language:
        cmd += f" --language {language}"
    if interactive:
        cmd += " --interactive"
    os.system(cmd)

@cli.command()
@click.option('--repo', help='Repository name (owner/repo)')
def quickdraw(repo):
    """Earn Quickdraw badge (5 minutes)"""
    cmd = f"python {os.path.dirname(__file__)}/quickdraw_automation.py quick-issue"
    if repo:
        cmd += f" --repo {repo}"
    os.system(cmd)

@cli.command()
@click.option('--name', help='Co-author name')
@click.option('--email', help='Co-author email')
def coauthor(name, email):
    """Generate co-author commit message (Pair Extraordinaire)"""
    cmd = f"python {os.path.dirname(__file__)}/coauthor_helper.py"
    if name and email:
        cmd += f" create-message --name '{name}' --email '{email}'"
    else:
        cmd += " guide"
    os.system(cmd)

@cli.command()
@click.option('--topic', help='Filter by topic')
@click.option('--language', help='Filter by language')
def discussions(topic, language):
    """Find GitHub discussions (Galaxy Brain)"""
    cmd = f"python {os.path.dirname(__file__)}/discussion_finder.py find-repos"
    if topic:
        cmd += f" --topic {topic}"
    if language:
        cmd += f" --language {language}"
    os.system(cmd)

@cli.group()
def guide():
    """Show guides for specific badges"""
    pass

@guide.command()
def quickdraw():
    """Quickdraw badge guide"""
    guide_file = os.path.join(os.path.dirname(__file__), '..', 'guides', 'quickdraw.md')
    if os.path.exists(guide_file):
        with open(guide_file, 'r') as f:
            content = f.read()
        click.echo_via_pager(content)
    else:
        click.echo(f"{Fore.RED}Guide file not found: {guide_file}")

@guide.command()  
def heart():
    """Heart On Your Sleeve badge guide"""
    guide_file = os.path.join(os.path.dirname(__file__), '..', 'guides', 'heart-on-your-sleeve.md')
    if os.path.exists(guide_file):
        with open(guide_file, 'r') as f:
            content = f.read()
        click.echo_via_pager(content)
    else:
        click.echo(f"{Fore.RED}Guide file not found: {guide_file}")

@guide.command()
def all():
    """List all available guides"""
    guides_dir = os.path.join(os.path.dirname(__file__), '..', 'guides')
    if os.path.exists(guides_dir):
        click.echo(f"{Fore.GREEN}📚 Available Badge Guides:")
        click.echo()
        for file in sorted(os.listdir(guides_dir)):
            if file.endswith('.md') and file != 'README.md':
                badge_name = file.replace('.md', '').replace('-', ' ').title()
                click.echo(f"  • {badge_name} - badge guide {file.replace('.md', '')}")
        click.echo()
        click.echo(f"{Fore.YELLOW}Use: badge guide <name> to view specific guides")
    else:
        click.echo(f"{Fore.RED}Guides directory not found")

@cli.command()
def tips():
    """Show quick tips for earning badges"""
    click.echo(f"{Fore.GREEN}🏆 Quick Badge Earning Tips")
    click.echo()
    click.echo(f"{Fore.CYAN}🎯 NEW: Comprehensive Badge Earning:")
    click.echo(f"  badge earn plan             # See personalized earning plan")
    click.echo(f"  badge earn execute          # Automatically earn all possible badges")
    click.echo(f"  badge earn all --execute    # Full automation with verification")
    click.echo()
    click.echo(f"{Fore.CYAN}🚀 Start Here (5-30 minutes):")
    click.echo(f"  1. badge quickdraw          # Easiest badge (5 min)")
    click.echo(f"  2. Create simple repo and merge PR without review (YOLO)")
    click.echo(f"  3. Sponsor someone $1/month (Public Sponsor)")
    click.echo()
    click.echo(f"{Fore.YELLOW}📈 Build Momentum (1-4 weeks):")
    click.echo(f"  1. badge find-repos         # Find contribution opportunities")
    click.echo(f"  2. Make your first merged PR (Heart On Your Sleeve)")
    click.echo(f"  3. Contribute to 2+ repos (Open Sourcerer)")
    click.echo()
    click.echo(f"{Fore.MAGENTA}🎯 Long Term (1-6 months):")
    click.echo(f"  1. badge discussions        # Answer GitHub discussions")
    click.echo(f"  2. badge coauthor          # Work with others")
    click.echo(f"  3. Build popular project (Starstruck)")
    click.echo()
    click.echo(f"{Fore.GREEN}Commands:")
    click.echo(f"  badge status               # Check your progress")
    click.echo(f"  badge earn all --execute   # Earn all possible badges automatically")
    click.echo(f"  badge guide all           # See all guides")
    click.echo(f"  badge --help              # Full command list")

@cli.command()
def setup():
    """Setup GitHub token and dependencies"""
    click.echo(f"{Fore.GREEN}🔧 GitHub Achievement Setup")
    click.echo()
    
    # Check if token is set
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        click.echo(f"{Fore.GREEN}✅ GitHub token is configured")
    else:
        click.echo(f"{Fore.RED}❌ GitHub token not found")
        click.echo()
        click.echo(f"{Fore.YELLOW}To set up your GitHub token:")
        click.echo("1. Go to https://github.com/settings/tokens")
        click.echo("2. Create a personal access token with 'repo' scope")
        click.echo("3. Set environment variable:")
        click.echo("   export GITHUB_TOKEN='your_token_here'")
        click.echo("4. Add to your shell profile (.bashrc, .zshrc, etc.)")
        click.echo()
    
    # Check dependencies
    try:
        import github
        import requests
        import tabulate
        click.echo(f"{Fore.GREEN}✅ Python dependencies installed")
    except ImportError as e:
        click.echo(f"{Fore.RED}❌ Missing dependencies: {e}")
        click.echo(f"{Fore.YELLOW}Install with: pip install -r requirements.txt")
        click.echo()
    
    # Check if guides exist
    guides_dir = os.path.join(os.path.dirname(__file__), '..', 'guides')
    if os.path.exists(guides_dir):
        click.echo(f"{Fore.GREEN}✅ Badge guides available")
    else:
        click.echo(f"{Fore.RED}❌ Badge guides not found")
    
    click.echo()
    if token and os.path.exists(guides_dir):
        click.echo(f"{Fore.GREEN}🎉 Setup complete! Try: badge tips")
    else:
        click.echo(f"{Fore.YELLOW}⚠️  Complete setup steps above, then run: badge tips")

@cli.command()
def dashboard():
    """Open GitHub achievement dashboard"""
    import webbrowser
    
    click.echo(f"{Fore.CYAN}Opening GitHub achievements in your browser...")
    
    # Try to get GitHub username
    try:
        if os.environ.get('GITHUB_TOKEN'):
            from github import Github
            g = Github(os.environ['GITHUB_TOKEN'])
            username = g.get_user().login
            url = f"https://github.com/{username}?tab=achievements"
        else:
            url = "https://github.com/settings/profile"
    except:
        url = "https://github.com/settings/profile"
    
    webbrowser.open(url)
    click.echo(f"{Fore.GREEN}✅ Opened: {url}")

@cli.group()
def earn():
    """Comprehensive badge earning commands"""
    pass

@earn.command()
@click.option('--execute', is_flag=True, help='Execute automated badge earning')
@click.option('--verify', is_flag=True, help='Verify progress after execution')
def all(execute, verify):
    """Create and execute comprehensive badge earning plan"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        click.echo(f"{Fore.RED}❌ GitHub token required. Run 'badge setup' first.")
        return
        
    cmd = f"python {os.path.dirname(__file__)}/badge_orchestrator.py earn-all"
    if execute:
        cmd += " --execute"
    if verify:
        cmd += " --verify"
    os.system(cmd)

@earn.command()
def plan():
    """Show badge earning plan without execution"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        click.echo(f"{Fore.RED}❌ GitHub token required. Run 'badge setup' first.")
        return
        
    cmd = f"python {os.path.dirname(__file__)}/badge_orchestrator.py plan"
    os.system(cmd)

@earn.command()
def execute():
    """Execute automated badge earning with verification"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        click.echo(f"{Fore.RED}❌ GitHub token required. Run 'badge setup' first.")
        return
        
    cmd = f"python {os.path.dirname(__file__)}/badge_orchestrator.py execute"
    os.system(cmd)

if __name__ == "__main__":
    cli()
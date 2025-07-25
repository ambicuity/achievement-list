#!/usr/bin/env python3
"""
Quickdraw Achievement Automation Tool

This script helps you achieve the Quickdraw badge by quickly managing issues and PRs.
Quickdraw badge: Close an issue or pull request within 5 minutes of opening.
"""

import os
import sys
import time
import click
import requests
from datetime import datetime, timedelta
from github import Github
from colorama import init, Fore, Style
from typing import List, Dict, Optional

init(autoreset=True)

class QuickdrawAutomation:
    def __init__(self, token: str):
        self.github = Github(token)
        self.token = token
        self.user = self.github.get_user()
        
    def create_and_close_issue_quickly(self, repo_name: str, delay_seconds: int = 30):
        """Create an issue and close it quickly for Quickdraw badge"""
        
        try:
            repo = self.github.get_repo(repo_name)
            
            # Create a simple issue
            issue_title = "docs: quick documentation improvement suggestion"
            issue_body = """## Summary
Quick suggestion for documentation improvement.

## Suggestion
This is a quick documentation improvement suggestion that can be implemented easily.

## Action
Closing this issue as it will be addressed in an upcoming PR.
"""
            
            print(f"{Fore.CYAN}Creating issue in {repo_name}...")
            issue = repo.create_issue(title=issue_title, body=issue_body)
            print(f"{Fore.GREEN}✅ Issue created: {issue.html_url}")
            
            # Wait for specified delay
            print(f"{Fore.YELLOW}⏳ Waiting {delay_seconds} seconds before closing...")
            time.sleep(delay_seconds)
            
            # Close the issue with a comment
            close_comment = "Closing this issue as the suggestion will be implemented in future documentation updates."
            issue.create_comment(close_comment)
            issue.edit(state='closed')
            
            print(f"{Fore.GREEN}✅ Issue closed successfully!")
            print(f"{Fore.MAGENTA}🏆 Quickdraw badge progress: Issue opened and closed within {delay_seconds} seconds!")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}")
            return False
            
    def find_own_repositories(self) -> List[Dict]:
        """Find user's own repositories suitable for quickdraw"""
        
        repos = []
        try:
            user_repos = self.user.get_repos(type='owner')
            
            for repo in user_repos:
                if not repo.private:  # Only public repos for achievements
                    repos.append({
                        'name': repo.full_name,
                        'description': repo.description or "No description",
                        'url': repo.html_url,
                        'issues_enabled': repo.has_issues
                    })
                    
        except Exception as e:
            print(f"{Fore.RED}Error fetching repositories: {e}")
            
        return repos
        
    def create_quick_pr_cycle(self, repo_name: str, delay_seconds: int = 60):
        """Create a simple PR and close it quickly"""
        
        print(f"{Fore.CYAN}Creating quick PR cycle for {repo_name}...")
        print(f"{Fore.YELLOW}Note: This creates a simple documentation PR that can be closed quickly")
        
        # Instructions for manual PR creation since we can't clone/push in this context
        instructions = f"""
{Fore.GREEN}Quick PR Instructions for {repo_name}:

1. Clone the repository:
   git clone https://github.com/{repo_name}.git
   cd {repo_name.split('/')[-1]}

2. Create a new branch:
   git checkout -b quickdraw/documentation-update

3. Make a simple change (add a comment or fix a typo):
   echo "<!-- Quick documentation update -->" >> README.md

4. Commit and push:
   git add .
   git commit -m "docs: quick documentation update"
   git push origin quickdraw/documentation-update

5. Create PR via GitHub web interface

6. Immediately close the PR with comment:
   "Closing this PR as the change will be implemented differently"

{Fore.MAGENTA}🏆 This will earn you the Quickdraw badge if done within 5 minutes!
"""
        
        print(instructions)
        return True
        
    def monitor_recent_activity(self):
        """Monitor recent issues and PRs for quickdraw opportunities"""
        
        print(f"{Fore.CYAN}🔍 Monitoring recent activity for quickdraw opportunities...")
        
        try:
            # Get recent issues from user's repositories
            user_repos = list(self.user.get_repos(type='owner'))[:5]  # Check first 5 repos
            
            recent_items = []
            
            for repo in user_repos:
                if not repo.has_issues:
                    continue
                    
                try:
                    # Get recent issues
                    issues = list(repo.get_issues(state='open', sort='created'))[:3]
                    for issue in issues:
                        time_diff = datetime.now() - issue.created_at.replace(tzinfo=None)
                        if time_diff.total_seconds() < 300:  # Less than 5 minutes old
                            recent_items.append({
                                'type': 'issue',
                                'repo': repo.full_name,
                                'title': issue.title,
                                'url': issue.html_url,
                                'age_seconds': time_diff.total_seconds(),
                                'number': issue.number
                            })
                            
                    # Get recent PRs
                    prs = list(repo.get_pulls(state='open', sort='created'))[:3]
                    for pr in prs:
                        time_diff = datetime.now() - pr.created_at.replace(tzinfo=None)
                        if time_diff.total_seconds() < 300:  # Less than 5 minutes old
                            recent_items.append({
                                'type': 'pr',
                                'repo': repo.full_name,
                                'title': pr.title,
                                'url': pr.html_url,
                                'age_seconds': time_diff.total_seconds(),
                                'number': pr.number
                            })
                            
                except Exception as e:
                    continue
                    
            if recent_items:
                print(f"{Fore.GREEN}🎯 Found {len(recent_items)} recent items for quickdraw:")
                for item in recent_items:
                    age_minutes = item['age_seconds'] / 60
                    remaining_time = 5 - age_minutes
                    print(f"  {item['type'].upper()} #{item['number']}: {item['title'][:50]}...")
                    print(f"    Age: {age_minutes:.1f} minutes | Remaining: {remaining_time:.1f} minutes")
                    print(f"    URL: {item['url']}")
                    print()
            else:
                print(f"{Fore.YELLOW}No recent items found for quickdraw opportunities")
                
        except Exception as e:
            print(f"{Fore.RED}Error monitoring activity: {e}")

@click.group()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.pass_context
def cli(ctx, token):
    """Quickdraw Achievement Automation Tool"""
    if not token:
        print(f"{Fore.RED}Error: GitHub token is required. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
        
    ctx.ensure_object(dict)
    ctx.obj['automation'] = QuickdrawAutomation(token)

@cli.command()
@click.option('--repo', help='Repository name (owner/repo)')
@click.option('--delay', default=30, help='Delay in seconds before closing (default: 30)')
@click.pass_context
def quick_issue(ctx, repo, delay):
    """Create and quickly close an issue for Quickdraw badge"""
    
    automation = ctx.obj['automation']
    
    if not repo:
        repos = automation.find_own_repositories()
        if not repos:
            print(f"{Fore.RED}❌ No suitable repositories found")
            return
            
        print(f"{Fore.CYAN}Your repositories:")
        for i, r in enumerate(repos, 1):
            status = "✅" if r['issues_enabled'] else "❌"
            print(f"  {i}. {status} {r['name']} - {r['description'][:50]}")
            
        choice = click.prompt("Select repository number", type=int)
        if 1 <= choice <= len(repos):
            repo = repos[choice - 1]['name']
        else:
            print(f"{Fore.RED}Invalid choice")
            return
            
    automation.create_and_close_issue_quickly(repo, delay)

@cli.command()
@click.option('--repo', help='Repository name (owner/repo)')
@click.pass_context  
def quick_pr(ctx, repo):
    """Get instructions for creating and quickly closing a PR"""
    
    automation = ctx.obj['automation']
    
    if not repo:
        repos = automation.find_own_repositories()
        if not repos:
            print(f"{Fore.RED}❌ No suitable repositories found")
            return
            
        print(f"{Fore.CYAN}Your repositories:")
        for i, r in enumerate(repos, 1):
            print(f"  {i}. {r['name']} - {r['description'][:50]}")
            
        choice = click.prompt("Select repository number", type=int)
        if 1 <= choice <= len(repos):
            repo = repos[choice - 1]['name']
        else:
            print(f"{Fore.RED}Invalid choice")
            return
            
    automation.create_quick_pr_cycle(repo)

@cli.command()
@click.pass_context
def monitor(ctx):
    """Monitor recent activity for quickdraw opportunities"""
    
    automation = ctx.obj['automation']
    automation.monitor_recent_activity()

@cli.command()
@click.pass_context
def guide(ctx):
    """Show Quickdraw badge earning guide"""
    
    guide_text = f"""
{Fore.GREEN}🏆 Quickdraw Badge Guide

{Fore.CYAN}What is Quickdraw?
Close an issue or pull request within 5 minutes of opening it.

{Fore.YELLOW}Strategies:

1. {Fore.MAGENTA}Own Repository Strategy (Recommended):
   - Create a simple issue in your own repository
   - Wait 30-60 seconds
   - Close the issue with a comment
   - This is the safest and most reliable method

2. {Fore.MAGENTA}Quick PR Strategy:
   - Create a simple documentation PR
   - Immediately close it with a reason
   - Good for repos where you made a mistake

3. {Fore.MAGENTA}Monitor Strategy:
   - Watch for your own recent issues/PRs
   - Close them quickly if appropriate

{Fore.RED}Important Notes:
- Only works with issues/PRs you created
- Must be closed within 5 minutes of creation
- Adding a closing comment is recommended for context
- Don't spam other people's repositories

{Fore.GREEN}Commands:
• quickdraw quick-issue --repo owner/repo    # Create and close issue
• quickdraw quick-pr --repo owner/repo       # Get PR instructions  
• quickdraw monitor                          # Check recent activity
"""
    
    print(guide_text)

if __name__ == "__main__":
    cli()
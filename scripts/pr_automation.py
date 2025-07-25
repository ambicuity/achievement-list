#!/usr/bin/env python3
"""
PR Automation Tool for GitHub Achievement Badges

This script helps automate pull request creation and management to earn:
- Heart On Your Sleeve badge
- Pull Shark badge
- Open Sourcerer badge
"""

import os
import sys
import time
import click
import requests
from github import Github
from colorama import init, Fore, Style
from typing import List, Dict, Optional

init(autoreset=True)

class PRAutomation:
    def __init__(self, token: str):
        self.github = Github(token)
        self.token = token
        self.user = self.github.get_user()
        
    def find_repositories_for_contribution(self, 
                                         language: Optional[str] = None, 
                                         good_first_issue: bool = True,
                                         min_stars: int = 10,
                                         max_results: int = 50) -> List[Dict]:
        """Find repositories suitable for contributions"""
        
        search_query = "is:public archived:false "
        
        if language:
            search_query += f"language:{language} "
            
        if good_first_issue:
            search_query += "label:\"good first issue\" OR label:\"help wanted\" "
            
        search_query += f"stars:>{min_stars}"
        
        print(f"{Fore.CYAN}Searching for repositories with query: {search_query}")
        
        repos = []
        try:
            search_result = self.github.search_repositories(search_query, sort="updated")
            
            for repo in search_result[:max_results]:
                # Skip if user already has PRs in this repo
                try:
                    prs = list(repo.get_pulls(state='all', head=f"{self.user.login}:"))
                    if len(prs) > 0:
                        continue
                except:
                    pass  # Repo might not allow access to PRs
                    
                repos.append({
                    'name': repo.full_name,
                    'description': repo.description or "No description",
                    'stars': repo.stargazers_count,
                    'language': repo.language,
                    'url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'open_issues': repo.open_issues_count
                })
                
        except Exception as e:
            print(f"{Fore.RED}Error searching repositories: {e}")
            
        return repos
        
    def suggest_contribution_types(self) -> List[str]:
        """Suggest types of contributions that are likely to be accepted"""
        return [
            "Fix typos in documentation",
            "Add missing documentation",
            "Update README files",
            "Fix broken links",
            "Add code comments",
            "Update dependencies",
            "Add tests for existing code",
            "Improve error messages",
            "Add example usage",
            "Fix formatting issues"
        ]
        
    def create_simple_pr_template(self, repo_name: str, contribution_type: str) -> Dict:
        """Create a template for a simple PR"""
        templates = {
            "documentation": {
                "title": "docs: improve documentation clarity",
                "body": """## Summary
This PR improves the documentation by:
- Fixing typos and grammar
- Adding clarity to existing descriptions
- Improving formatting

## Changes
- Updated README.md for better readability
- Fixed typos in documentation files
- Improved code examples

## Testing
- [x] Documentation builds without errors
- [x] All links are working
- [x] Examples are valid""",
                "files": ["README.md", "docs/"]
            },
            "readme": {
                "title": "docs: enhance README with examples and clarity",
                "body": """## Summary
This PR enhances the README file with:
- Better examples
- Clearer installation instructions
- Improved formatting

## Changes
- Added usage examples
- Improved installation section
- Fixed formatting issues
- Added badges if missing

## Testing
- [x] All examples work as expected
- [x] Installation instructions are accurate""",
                "files": ["README.md"]
            },
            "typos": {
                "title": "fix: correct typos and improve text clarity",
                "body": """## Summary
This PR fixes various typos and improves text clarity throughout the project.

## Changes
- Fixed spelling errors
- Improved grammar
- Enhanced readability

## Testing
- [x] Verified all changes maintain original meaning
- [x] No functional changes made""",
                "files": ["*.md", "docs/", "comments"]
            }
        }
        
        return templates.get(contribution_type, templates["documentation"])

@click.command()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--language', help='Filter repositories by programming language')
@click.option('--max-results', default=20, help='Maximum number of repositories to show')
@click.option('--min-stars', default=10, help='Minimum number of stars for repositories')
@click.option('--interactive', is_flag=True, help='Interactive mode for repository selection')
def main(token, language, max_results, min_stars, interactive):
    """GitHub PR Automation Tool for earning achievement badges"""
    
    if not token:
        print(f"{Fore.RED}Error: GitHub token is required. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
        
    print(f"{Fore.GREEN}🚀 GitHub Achievement PR Automation Tool")
    print(f"{Fore.YELLOW}Target badges: Heart On Your Sleeve, Pull Shark, Open Sourcerer")
    print()
    
    automation = PRAutomation(token)
    
    print(f"{Fore.CYAN}👤 Authenticated as: {automation.user.login}")
    print()
    
    # Find suitable repositories
    print(f"{Fore.MAGENTA}🔍 Finding repositories for contributions...")
    repos = automation.find_repositories_for_contribution(
        language=language,
        min_stars=min_stars,
        max_results=max_results
    )
    
    if not repos:
        print(f"{Fore.RED}❌ No suitable repositories found. Try different search criteria.")
        return
        
    print(f"{Fore.GREEN}✅ Found {len(repos)} suitable repositories:")
    print()
    
    # Display repositories
    for i, repo in enumerate(repos, 1):
        print(f"{Fore.CYAN}{i:2d}. {repo['name']}")
        print(f"    ⭐ {repo['stars']} stars | 🐛 {repo['open_issues']} issues | 💻 {repo['language'] or 'Mixed'}")
        print(f"    📝 {repo['description'][:80]}...")
        print(f"    🔗 {repo['url']}")
        print()
        
    # Show contribution suggestions
    print(f"{Fore.YELLOW}💡 Suggested contribution types:")
    suggestions = automation.suggest_contribution_types()
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion}")
    print()
    
    # Show PR templates
    print(f"{Fore.MAGENTA}📝 PR Template Examples:")
    template = automation.create_simple_pr_template("example/repo", "documentation")
    print(f"{Fore.GREEN}Title: {template['title']}")
    print(f"{Fore.CYAN}Body preview:")
    print(template['body'][:200] + "...")
    print()
    
    print(f"{Fore.YELLOW}⚡ Quick Start Guide:")
    print("1. Pick a repository from the list above")
    print("2. Clone it locally: git clone [clone_url]")
    print("3. Create a branch: git checkout -b improvement/docs-update")
    print("4. Make small improvements (fix typos, improve docs)")
    print("5. Commit and push: git commit -m 'docs: fix typos' && git push")
    print("6. Create PR through GitHub web interface")
    print("7. Repeat for different repositories to earn badges!")
    print()
    print(f"{Fore.GREEN}🏆 Badge Progress:")
    print("• Heart On Your Sleeve: Need 1+ merged PR")
    print("• Pull Shark: Need 2+ merged PRs (Bronze: 16, Silver: 128, Gold: 1024)")
    print("• Open Sourcerer: Need PRs in 2+ different repos (Bronze: 3, Silver: 4+)")

if __name__ == "__main__":
    main()
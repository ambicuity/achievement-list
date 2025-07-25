#!/usr/bin/env python3
"""
Co-Author Helper for Pair Extraordinaire Badge

This script helps set up co-authored commits to earn the Pair Extraordinaire badge.
Pair Extraordinaire: Coauthored commits on merged pull request (1, 10, 24, 48 for tiers)
"""

import os
import sys
import click
import re
from colorama import init, Fore, Style
from typing import List, Dict, Optional

init(autoreset=True)

class CoAuthorHelper:
    def __init__(self):
        self.coauthor_template = "Co-authored-by: {name} <{email}>"
        
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def generate_coauthor_line(self, name: str, email: str) -> str:
        """Generate a co-author line for commit messages"""
        if not self.validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
            
        return self.coauthor_template.format(name=name, email=email)
        
    def create_commit_message(self, title: str, description: str = "", coauthors: List[Dict] = None) -> str:
        """Create a properly formatted commit message with co-authors"""
        
        message_parts = [title]
        
        if description:
            message_parts.append("")  # Empty line
            message_parts.append(description)
            
        if coauthors:
            message_parts.append("")  # Empty line before co-authors
            for author in coauthors:
                coauthor_line = self.generate_coauthor_line(author['name'], author['email'])
                message_parts.append(coauthor_line)
                
        return "\n".join(message_parts)
        
    def find_github_collaborators(self, username: str) -> List[str]:
        """Get suggested GitHub usernames for collaboration"""
        
        # Common GitHub usernames for collaboration examples
        suggestions = [
            f"{username}-bot",
            f"{username}-collaborator", 
            "github-actions[bot]",
            "dependabot[bot]",
            "renovate[bot]"
        ]
        
        return suggestions
        
    def get_github_noreply_email(self, username: str, user_id: Optional[str] = None) -> str:
        """Generate GitHub no-reply email format"""
        if user_id:
            return f"{user_id}+{username}@users.noreply.github.com"
        else:
            return f"{username}@users.noreply.github.com"
            
    def create_pair_programming_guide(self) -> str:
        """Generate a guide for pair programming and co-authoring"""
        
        guide = f"""
{Fore.GREEN}🤝 Pair Extraordinaire Badge Guide

{Fore.CYAN}What is Pair Extraordinaire?
Create co-authored commits on merged pull requests.

{Fore.YELLOW}Badge Tiers:
• Default: 1 co-authored commit
• Bronze: 10 co-authored commits  
• Silver: 24 co-authored commits
• Gold: 48 co-authored commits

{Fore.MAGENTA}How to Add Co-Authors:

1. {Fore.CYAN}In Commit Messages:
   Add co-author lines at the end of your commit message:
   
   git commit -m "feat: add new feature
   
   This commit adds a new feature with help from collaborators.
   
   Co-authored-by: Name <email@example.com>
   Co-authored-by: Another Person <person@example.com>"

2. {Fore.CYAN}Using Git Trailer Format:
   git commit -m "fix: resolve bug" -m "Co-authored-by: Name <email@example.com>"

3. {Fore.CYAN}GitHub Web Interface:
   When creating a PR, add co-authors in the commit message or PR description.

{Fore.RED}Important Notes:
• Co-authors must have valid GitHub accounts
• Email should match their GitHub email or use no-reply format
• All co-authored commits must be in merged PRs
• You can co-author with bots (dependabot, renovate, etc.)

{Fore.GREEN}Strategies for Earning the Badge:

1. {Fore.MAGENTA}Real Collaboration:
   • Work with friends/colleagues on open source projects
   • Participate in hackathons with teammates
   • Contribute to projects where maintainers help with commits

2. {Fore.MAGENTA}Bot Collaboration:
   • Co-author with dependabot when updating dependencies
   • Work with GitHub Actions bots on automated updates
   • Collaborate with renovate bot on dependency updates

3. {Fore.MAGENTA}Mentoring/Learning:
   • Co-author commits when learning from mentors
   • Credit code reviewers who provide significant input
   • Acknowledge pair programming sessions

{Fore.YELLOW}Example Commit Messages:

Basic co-authoring:
```
docs: update README with installation guide

Added comprehensive installation instructions.

Co-authored-by: Jane Doe <jane@example.com>
```

Multiple co-authors:
```
feat: implement user authentication

- Add login/logout functionality
- Include password hashing
- Add session management

Co-authored-by: John Smith <john@users.noreply.github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```
"""
        return guide

@click.group()
def cli():
    """Co-Author Helper for Pair Extraordinaire Badge"""
    pass

@cli.command()
@click.option('--title', prompt='Commit title', help='Main commit message title')
@click.option('--description', help='Optional commit description')
@click.option('--name', multiple=True, help='Co-author name (can be used multiple times)')
@click.option('--email', multiple=True, help='Co-author email (can be used multiple times)')
def create_message(title, description, name, email):
    """Create a commit message with co-authors"""
    
    helper = CoAuthorHelper()
    
    if len(name) != len(email):
        print(f"{Fore.RED}❌ Error: Number of names must match number of emails")
        return
        
    coauthors = []
    for n, e in zip(name, email):
        try:
            # Validate email
            helper.validate_email(e)
            coauthors.append({'name': n, 'email': e})
        except ValueError as ve:
            print(f"{Fore.RED}❌ {ve}")
            return
            
    message = helper.create_commit_message(title, description, coauthors)
    
    print(f"{Fore.GREEN}✅ Generated commit message:")
    print(f"{Fore.CYAN}" + "="*50)
    print(message)
    print(f"{Fore.CYAN}" + "="*50)
    
    print(f"\n{Fore.YELLOW}💡 To use this commit message:")
    print(f"git commit -m \"{message.replace(chr(10), chr(10) + '                ')}\"")

@cli.command()
@click.option('--username', prompt='GitHub username', help='GitHub username for suggestions')
@click.option('--user-id', help='GitHub user ID for no-reply email format')
def suggest_coauthors(username, user_id):
    """Get suggestions for co-author collaborations"""
    
    helper = CoAuthorHelper()
    
    print(f"{Fore.GREEN}🤝 Co-Author Suggestions for {username}:")
    print()
    
    # Bot suggestions
    print(f"{Fore.CYAN}Bot Collaborators (Always Available):")
    bots = [
        ("dependabot[bot]", "49699333+dependabot[bot]@users.noreply.github.com"),
        ("github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com"),
        ("renovate[bot]", "29139614+renovate[bot]@users.noreply.github.com"),
        ("imgbot[bot]", "31427895+imgbot[bot]@users.noreply.github.com")
    ]
    
    for bot_name, bot_email in bots:
        print(f"  • {bot_name}")
        print(f"    {bot_email}")
        print(f"    Example: Co-authored-by: {bot_name} <{bot_email}>")
        print()
    
    # GitHub no-reply email formats
    print(f"{Fore.MAGENTA}Your GitHub No-Reply Email Formats:")
    noreply_basic = helper.get_github_noreply_email(username)
    print(f"  • Basic: {noreply_basic}")
    
    if user_id:
        noreply_with_id = helper.get_github_noreply_email(username, user_id)
        print(f"  • With ID: {noreply_with_id}")
    
    print()
    print(f"{Fore.YELLOW}💡 Tips:")
    print("• Use bot emails when updating dependencies or automation")
    print("• Co-author with real collaborators when pair programming")
    print("• Check GitHub profiles for public no-reply email formats")
    print("• All co-authored commits must be in merged PRs to count")

@cli.command() 
@click.option('--name', prompt='Co-author name', help='Name of the co-author')
@click.option('--email', prompt='Co-author email', help='Email of the co-author') 
def validate_coauthor(name, email):
    """Validate co-author information"""
    
    helper = CoAuthorHelper()
    
    try:
        coauthor_line = helper.generate_coauthor_line(name, email)
        print(f"{Fore.GREEN}✅ Valid co-author format:")
        print(f"{Fore.CYAN}{coauthor_line}")
        
        print(f"\n{Fore.YELLOW}💡 Usage in commit:")
        example_commit = helper.create_commit_message(
            "feat: example commit",
            "This is an example commit with co-author.",
            [{'name': name, 'email': email}]
        )
        print(f"{Fore.MAGENTA}git commit -m \"{example_commit.replace(chr(10), chr(10) + '               ')}\"")
        
    except ValueError as e:
        print(f"{Fore.RED}❌ Invalid co-author: {e}")

@cli.command()
def guide():
    """Show comprehensive Pair Extraordinaire badge guide"""
    
    helper = CoAuthorHelper()
    guide_text = helper.create_pair_programming_guide()
    print(guide_text)

@cli.command()
def examples():
    """Show practical examples of co-authored commits"""
    
    examples_text = f"""
{Fore.GREEN}📝 Practical Co-Authoring Examples

{Fore.CYAN}1. Working with Dependabot:
When dependabot creates a PR, you can co-author additional commits:

```bash
git commit -m "chore: update dependencies and fix breaking changes

Fixed compatibility issues after dependency updates.

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>"
```

{Fore.CYAN}2. Pair Programming Session:
```bash
git commit -m "feat: implement user search functionality

Added search with filters and pagination.
Implemented during pair programming session.

Co-authored-by: Alice Johnson <alice@company.com>
Co-authored-by: Bob Smith <bob@users.noreply.github.com>"
```

{Fore.CYAN}3. Code Review Collaboration:
```bash
git commit -m "fix: resolve memory leak in data processing

Applied suggestions from code review.

Co-authored-by: Senior Dev <senior@users.noreply.github.com>"
```

{Fore.CYAN}4. Multiple Contributors:
```bash
git commit -m "docs: comprehensive API documentation update

- Updated all endpoint descriptions
- Added example requests/responses  
- Fixed formatting issues

Co-authored-by: Technical Writer <writer@company.com>
Co-authored-by: QA Engineer <qa@company.com>
Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"
```

{Fore.YELLOW}💡 Pro Tips:

• Use different co-authors across multiple commits
• Mix real collaborators with bots for variety
• Ensure all co-authored commits are in merged PRs
• Credit reviewers who provide substantial input
• Use consistent email formats (preferably no-reply)
"""
    
    print(examples_text)

if __name__ == "__main__":
    cli()
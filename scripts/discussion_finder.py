#!/usr/bin/env python3
"""
Discussion Finder for Galaxy Brain Badge

This script helps find GitHub discussions to participate in and earn the Galaxy Brain badge.
Galaxy Brain: Answer a discussion (get an accepted answer) - 2, 8, 16, 32 for tiers
"""

import os
import sys
import click
import requests
from datetime import datetime, timedelta
from github import Github
from colorama import init, Fore, Style
from typing import List, Dict, Optional
import json

init(autoreset=True)

class DiscussionFinder:
    def __init__(self, token: str):
        self.github = Github(token)
        self.token = token
        self.user = self.github.get_user()
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def search_repositories_with_discussions(self, 
                                           topic: Optional[str] = None,
                                           language: Optional[str] = None,
                                           min_stars: int = 100,
                                           max_results: int = 20) -> List[Dict]:
        """Find repositories that have discussions enabled"""
        
        search_query = "is:public archived:false "
        
        if topic:
            search_query += f"topic:{topic} "
        if language:
            search_query += f"language:{language} "
            
        search_query += f"stars:>{min_stars}"
        
        print(f"{Fore.CYAN}Searching for repositories with discussions...")
        
        repos_with_discussions = []
        try:
            search_result = self.github.search_repositories(search_query, sort="updated")
            
            for repo in search_result[:max_results * 2]:  # Get more to filter
                # Check if discussions are enabled (GitHub API doesn't directly expose this)
                # We'll use a heuristic approach
                try:
                    # Try to access discussions endpoint
                    discussions_url = f"https://api.github.com/repos/{repo.full_name}/discussions"
                    response = requests.get(discussions_url, headers=self.headers)
                    
                    if response.status_code == 200:
                        discussions_data = response.json()
                        
                        repos_with_discussions.append({
                            'name': repo.full_name,
                            'description': repo.description or "No description",
                            'stars': repo.stargazers_count,
                            'language': repo.language,
                            'url': repo.html_url,
                            'discussions_url': f"{repo.html_url}/discussions",
                            'topics': list(repo.get_topics())[:3],  # First 3 topics
                            'open_discussions': len(discussions_data) if isinstance(discussions_data, list) else 0
                        })
                        
                        if len(repos_with_discussions) >= max_results:
                            break
                            
                except Exception:
                    continue  # Skip repos where we can't access discussions
                    
        except Exception as e:
            print(f"{Fore.RED}Error searching repositories: {e}")
            
        return repos_with_discussions
        
    def get_discussion_categories(self) -> List[str]:
        """Get common discussion categories to look for"""
        return [
            "Q&A",
            "General", 
            "Ideas",
            "Show and tell",
            "Help",
            "Support",
            "Feature requests",
            "Announcements",
            "Discussions"
        ]
        
    def generate_helpful_responses(self) -> Dict[str, List[str]]:
        """Generate templates for helpful discussion responses"""
        
        return {
            "troubleshooting": [
                "Have you tried checking the logs for error messages?",
                "Could you share your configuration file (with sensitive data removed)?",
                "This looks like a version compatibility issue. What version are you using?",
                "I've seen this before. Try clearing your cache and restarting.",
                "Check if you have the required dependencies installed.",
                "Make sure your environment variables are set correctly.",
                "This might be related to file permissions. Can you check that?",
                "Try running in verbose mode to see more detailed output."
            ],
            "feature_requests": [
                "This is an interesting idea! Have you considered the impact on existing users?",
                "You might want to check if there are any existing issues or PRs for this.",
                "This could be implemented as a plugin/extension first.",
                "Consider creating a minimal working example to demonstrate the need.",
                "Have you looked at how other similar projects handle this?",
                "This would need careful documentation and migration guides.",
                "Consider the performance implications of this change."
            ],
            "general_help": [
                "Welcome to the community! Here are some resources to get started:",
                "The documentation covers this topic in section X.",
                "You might find the examples in the repository helpful.",
                "Check out the FAQ for common questions like this.",
                "The community chat/Discord might be helpful for real-time help.",
                "Consider searching existing issues for similar problems.",
                "Make sure you're using the latest version before reporting bugs."
            ],
            "best_practices": [
                "Here's the recommended approach for this use case:",
                "Consider following the project's coding standards for consistency.",
                "Make sure to include tests for any new functionality.",
                "Documentation updates are always appreciated alongside code changes.",
                "Consider the security implications of this approach.",
                "Performance testing would be valuable for this change.",
                "Make sure to handle edge cases and error conditions."
            ]
        }
        
    def suggest_discussion_topics(self, language: str = None) -> List[str]:
        """Suggest topics to look for in discussions"""
        
        general_topics = [
            "getting-started", "documentation", "api", "configuration",
            "deployment", "testing", "performance", "security", "best-practices",
            "migration", "troubleshooting", "examples", "tutorials"
        ]
        
        language_specific = {
            "Python": ["pip", "virtualenv", "django", "flask", "pytest", "packaging"],
            "JavaScript": ["npm", "webpack", "react", "vue", "node", "typescript"],
            "Java": ["maven", "gradle", "spring", "junit", "deployment"],
            "Go": ["modules", "testing", "concurrency", "performance"],
            "Rust": ["cargo", "ownership", "async", "performance"],
            "C++": ["cmake", "memory", "performance", "compilation"],
            "Ruby": ["gem", "rails", "bundler", "testing"]
        }
        
        topics = general_topics.copy()
        if language and language in language_specific:
            topics.extend(language_specific[language])
            
        return topics

@click.group()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.pass_context
def cli(ctx, token):
    """Discussion Finder for Galaxy Brain Badge"""
    if not token:
        print(f"{Fore.RED}Error: GitHub token is required. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
        
    ctx.ensure_object(dict)
    ctx.obj['finder'] = DiscussionFinder(token)

@cli.command()
@click.option('--topic', help='Filter by repository topic')
@click.option('--language', help='Filter by programming language')
@click.option('--min-stars', default=100, help='Minimum stars for repositories')
@click.option('--max-results', default=15, help='Maximum number of repositories to show')
@click.pass_context
def find_repos(ctx, topic, language, min_stars, max_results):
    """Find repositories with active discussions"""
    
    finder = ctx.obj['finder']
    
    print(f"{Fore.GREEN}🔍 Finding repositories with discussions enabled...")
    print(f"{Fore.YELLOW}👤 Authenticated as: {finder.user.login}")
    print()
    
    repos = finder.search_repositories_with_discussions(
        topic=topic,
        language=language, 
        min_stars=min_stars,
        max_results=max_results
    )
    
    if not repos:
        print(f"{Fore.RED}❌ No repositories with discussions found")
        print(f"{Fore.YELLOW}💡 Try different search criteria or lower the star threshold")
        return
        
    print(f"{Fore.GREEN}✅ Found {len(repos)} repositories with discussions:")
    print()
    
    for i, repo in enumerate(repos, 1):
        print(f"{Fore.CYAN}{i:2d}. {repo['name']}")
        print(f"    ⭐ {repo['stars']} stars | 💻 {repo['language'] or 'Mixed'}")
        print(f"    📝 {repo['description'][:80]}...")
        if repo['topics']:
            print(f"    🏷️  Topics: {', '.join(repo['topics'])}")
        print(f"    💬 Discussions: {repo['discussions_url']}")
        print()
        
    print(f"{Fore.MAGENTA}💡 Next Steps:")
    print("1. Visit the discussions pages of interesting repositories")
    print("2. Look for unanswered questions you can help with")
    print("3. Provide helpful, detailed answers")
    print("4. Wait for the discussion author to mark your answer as helpful")
    print("5. Repeat to earn higher badge tiers!")

@cli.command()
@click.option('--category', help='Discussion category to focus on')
@click.pass_context
def response_templates(ctx, category):
    """Get helpful response templates for discussions"""
    
    finder = ctx.obj['finder']
    responses = finder.generate_helpful_responses()
    
    print(f"{Fore.GREEN}💬 Discussion Response Templates")
    print()
    
    if category and category.lower().replace(' ', '_') in responses:
        cat_key = category.lower().replace(' ', '_')
        print(f"{Fore.CYAN}📂 {category.title()} Responses:")
        for i, template in enumerate(responses[cat_key], 1):
            print(f"  {i}. {template}")
        print()
    else:
        for cat_name, templates in responses.items():
            print(f"{Fore.CYAN}📂 {cat_name.replace('_', ' ').title()}:")
            for i, template in enumerate(templates[:3], 1):  # Show first 3
                print(f"  {i}. {template}")
            if len(templates) > 3:
                print(f"     ... and {len(templates) - 3} more")
            print()
            
    print(f"{Fore.YELLOW}💡 Tips for Galaxy Brain Badge:")
    print("• Provide detailed, helpful answers")
    print("• Include code examples when relevant")
    print("• Link to documentation or resources")
    print("• Be patient and supportive")
    print("• Follow up if needed")
    print("• Wait for the author to mark answers as helpful")

@cli.command()
@click.option('--language', help='Programming language for specific topics')
@click.pass_context
def suggest_topics(ctx, language):
    """Get suggested topics to look for in discussions"""
    
    finder = ctx.obj['finder']
    topics = finder.suggest_discussion_topics(language)
    categories = finder.get_discussion_categories()
    
    print(f"{Fore.GREEN}🎯 Suggested Discussion Topics")
    print()
    
    print(f"{Fore.CYAN}📂 Common Discussion Categories:")
    for cat in categories:
        print(f"  • {cat}")
    print()
    
    print(f"{Fore.MAGENTA}🔍 Search Keywords:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i:2d}. {topic}")
        if i % 10 == 0:  # Line break every 10 items
            print()
            
    print(f"\n{Fore.YELLOW}💡 Discussion Search Strategy:")
    print("1. Look for questions tagged with these topics")
    print("2. Focus on unanswered or partially answered discussions")
    print("3. Choose topics you have expertise in")
    print("4. Sort by 'recently updated' to find active discussions")
    print("5. Read the full question before answering")

@cli.command()
@click.pass_context
def guide(ctx):
    """Show comprehensive Galaxy Brain badge guide"""
    
    guide_text = f"""
{Fore.GREEN}🧠 Galaxy Brain Badge Guide

{Fore.CYAN}What is Galaxy Brain?
Answer a discussion and get it marked as helpful/accepted.

{Fore.YELLOW}Badge Tiers:
• Default: 2 accepted answers
• Bronze: 8 accepted answers
• Silver: 16 accepted answers  
• Gold: 32 accepted answers

{Fore.MAGENTA}How to Earn Galaxy Brain:

1. {Fore.CYAN}Find Active Discussions:
   • Look for repositories with discussions enabled
   • Focus on Q&A and Help categories
   • Search for unanswered questions
   • Filter by topics you know well

2. {Fore.CYAN}Provide Quality Answers:
   • Read the question thoroughly
   • Provide detailed, helpful responses
   • Include code examples when relevant
   • Link to relevant documentation
   • Be respectful and supportive

3. {Fore.CYAN}Get Answers Marked as Helpful:
   • Wait for the discussion author to respond
   • Follow up with clarifications if needed
   • The author must mark your answer as "helpful"
   • Only accepted/helpful answers count toward the badge

{Fore.RED}Important Notes:
• Only works in repositories with discussions enabled
• Your answer must be marked as helpful by the discussion author
• Spam or low-quality answers won't count
• Be genuine and helpful, don't just try to game the system

{Fore.GREEN}Strategies for Success:

1. {Fore.MAGENTA}Focus on Your Expertise:
   • Answer questions in technologies you know well
   • Share your practical experience
   • Provide tested solutions

2. {Fore.MAGENTA}Be Comprehensive:
   • Explain the why, not just the how
   • Include multiple approaches when relevant
   • Consider edge cases and potential issues

3. {Fore.MAGENTA}Follow Community Guidelines:
   • Be respectful and inclusive
   • Stay on topic
   • Help others learn, don't just solve problems

{Fore.CYAN}Best Repositories for Discussions:
• Popular open source projects (React, Vue, Django, etc.)
• Developer tools and frameworks
• Documentation projects
• Learning resources and tutorials
• Community-driven projects

{Fore.YELLOW}Pro Tips:
• Sort discussions by "recently updated" for active ones
• Look for discussions with 0 or few responses
• Engage in discussions about topics you're passionate about
• Be patient - it may take time for authors to mark answers
• Quality over quantity - focus on helpful answers
"""
    
    print(guide_text)

@cli.command()
@click.pass_context
def examples(ctx):
    """Show examples of good discussion answers"""
    
    examples_text = f"""
{Fore.GREEN}📝 Examples of Good Discussion Answers

{Fore.CYAN}1. Troubleshooting Example:
{Fore.WHITE}Question: "Getting 'ModuleNotFoundError' when importing my package"

{Fore.GREEN}Good Answer:
"This error typically occurs when Python can't find your module. Here are the most common causes and solutions:

1. **Check your PYTHONPATH**: Make sure your package directory is in Python's path
   ```bash
   export PYTHONPATH="${{PYTHONPATH}}:/path/to/your/package"
   ```

2. **Verify package structure**: Ensure you have `__init__.py` files in your directories
   ```
   mypackage/
   ├── __init__.py
   ├── module1.py
   └── subpackage/
       ├── __init__.py
       └── module2.py
   ```

3. **Install in development mode**: If it's your own package
   ```bash
   pip install -e .
   ```

Could you share your directory structure and import statement? That would help identify the specific issue."

{Fore.CYAN}2. Feature Request Discussion:
{Fore.WHITE}Question: "Would it be possible to add dark mode support?"

{Fore.GREEN}Good Answer:
"Great suggestion! Dark mode is definitely a popular feature. Here's what this would involve:

**Implementation considerations:**
- CSS custom properties for theming
- User preference detection/storage
- Accessibility compliance (contrast ratios)
- Integration with system preferences

**Potential approach:**
1. Create CSS variables for colors
2. Add a theme toggle component
3. Use localStorage to persist preference
4. Respect `prefers-color-scheme` media query

**Similar implementations:**
- GitHub's approach: [link to GitHub's implementation]
- Material-UI theming: [documentation link]

I'd be happy to help implement this! Would you prefer a PR that starts with basic dark mode, or should we plan for a full theming system?"

{Fore.CYAN}3. Best Practices Question:
{Fore.WHITE}Question: "What's the best way to structure a large React application?"

{Fore.GREEN}Good Answer:
"Great question! Here's a scalable structure I've used successfully in large React apps:

**Recommended structure:**
```
src/
├── components/           # Reusable UI components
│   ├── Button/
│   ├── Modal/
│   └── index.js
├── features/            # Feature-based organization
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── index.js
│   └── dashboard/
├── shared/              # Shared utilities
│   ├── hooks/
│   ├── utils/
│   └── constants/
├── store/               # State management
└── App.js
```

**Key principles:**
1. **Feature-based organization**: Group related files together
2. **Component co-location**: Keep components near their usage
3. **Shared utilities**: Extract common functionality
4. **Clear exports**: Use index.js files for clean imports

**Resources:**
- [Link to React documentation]
- [Example repository with this structure]

This structure scales well to 50+ developers and hundreds of components in my experience."

{Fore.YELLOW}💡 What Makes These Good:
• Detailed, actionable advice
• Code examples and structure
• Multiple solutions/approaches  
• Links to relevant resources
• Personal experience shared
• Follow-up questions to help more
"""
    
    print(examples_text)

if __name__ == "__main__":
    cli()
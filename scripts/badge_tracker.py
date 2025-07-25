#!/usr/bin/env python3
"""
Badge Tracker for GitHub Achievement Badges

This script tracks your progress towards GitHub achievement badges.
"""

import os
import sys
import json
import click
import requests
from datetime import datetime, timedelta
from github import Github
from colorama import init, Fore, Style
from tabulate import tabulate
from typing import Dict, List, Optional

init(autoreset=True)

class BadgeTracker:
    def __init__(self, token: str):
        self.github = Github(token)
        self.token = token
        self.user = self.github.get_user()
        
        # Badge definitions with requirements
        self.badges = {
            "Heart On Your Sleeve": {
                "description": "Submit a pull request that gets merged",
                "tiers": {"Default": 1, "Bronze": 2, "Silver": 4, "Gold": 8},
                "check_method": "count_merged_prs"
            },
            "Open Sourcerer": {
                "description": "User had PRs merged in multiple public repositories",
                "tiers": {"Default": 1, "Bronze": 2, "Silver": 3, "Gold": 4},
                "check_method": "count_repos_with_merged_prs"
            },
            "Starstruck": {
                "description": "Created a repository that has many stars",
                "tiers": {"Default": 16, "Bronze": 128, "Silver": 512, "Gold": 4096},
                "check_method": "count_max_stars"
            },
            "Quickdraw": {
                "description": "Closed an issue/pull request within 5 minutes of opening",
                "tiers": {"Default": 1},
                "check_method": "check_quickdraw"
            },
            "Pair Extraordinaire": {
                "description": "Coauthored commits on merged pull request",
                "tiers": {"Default": 1, "Bronze": 10, "Silver": 24, "Gold": 48},
                "check_method": "count_coauthored_commits"
            },
            "Pull Shark": {
                "description": "Opened a pull request that has been merged",
                "tiers": {"Default": 2, "Bronze": 16, "Silver": 128, "Gold": 1024},
                "check_method": "count_merged_prs"
            },
            "Galaxy Brain": {
                "description": "Answered a discussion (got an accepted answer)",
                "tiers": {"Default": 2, "Bronze": 8, "Silver": 16, "Gold": 32},
                "check_method": "count_discussion_answers"
            },
            "YOLO": {
                "description": "Merged a pull request without a review",
                "tiers": {"Default": 1},
                "check_method": "check_yolo_merges"
            },
            "Public Sponsor": {
                "description": "Sponsored an open source contributor through GitHub Sponsors",
                "tiers": {"Default": 1},
                "check_method": "check_sponsorships"
            }
        }
        
    def count_merged_prs(self) -> int:
        """Count merged pull requests by the user"""
        count = 0
        try:
            # Search for merged PRs by this user
            query = f"type:pr author:{self.user.login} is:merged"
            prs = self.github.search_issues(query)
            count = prs.totalCount
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not count merged PRs: {e}")
        return count
        
    def count_repos_with_merged_prs(self) -> int:
        """Count repositories where user has merged PRs"""
        repos = set()
        try:
            query = f"type:pr author:{self.user.login} is:merged"
            prs = self.github.search_issues(query)
            
            # Get first 100 PRs to check repos (API limitation)
            for pr in prs[:100]:
                if hasattr(pr, 'repository'):
                    repos.add(pr.repository.full_name)
                    
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not count repositories with merged PRs: {e}")
            
        return len(repos)
        
    def count_max_stars(self) -> int:
        """Find the repository with the most stars"""
        max_stars = 0
        try:
            repos = self.user.get_repos(type='owner')
            for repo in repos:
                if not repo.private and repo.stargazers_count > max_stars:
                    max_stars = repo.stargazers_count
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not count stars: {e}")
            
        return max_stars
        
    def check_quickdraw(self) -> int:
        """Check for quickdraw achievements (simplified check)"""
        # This is a simplified check - real implementation would need detailed timing analysis
        print(f"{Fore.YELLOW}Note: Quickdraw detection requires manual verification of timing")
        return 0  # Cannot reliably detect without detailed API access
        
    def count_coauthored_commits(self) -> int:
        """Count co-authored commits (simplified check)"""
        # This would require detailed commit analysis across all repositories
        print(f"{Fore.YELLOW}Note: Co-authored commit counting requires detailed commit analysis")
        return 0  # Cannot reliably detect without repo-by-repo analysis
        
    def count_discussion_answers(self) -> int:
        """Count discussion answers (simplified check)"""
        # GitHub Discussions API access is limited
        print(f"{Fore.YELLOW}Note: Discussion answer counting requires Discussions API access")
        return 0  # Cannot reliably detect without specific API endpoints
        
    def check_yolo_merges(self) -> int:
        """Check for YOLO merges (simplified check)"""
        print(f"{Fore.YELLOW}Note: YOLO merge detection requires detailed PR analysis")
        return 0  # Cannot reliably detect without detailed review analysis
        
    def check_sponsorships(self) -> int:
        """Check for GitHub sponsorships"""
        print(f"{Fore.YELLOW}Note: Sponsorship data is private and cannot be checked via API")
        return 0  # Sponsorship data is private
        
    def get_badge_progress(self) -> Dict:
        """Get progress for all badges"""
        progress = {}
        
        print(f"{Fore.CYAN}Analyzing badge progress for {self.user.login}...")
        print(f"{Fore.YELLOW}Note: Some badges require manual verification due to API limitations")
        print()
        
        for badge_name, badge_info in self.badges.items():
            print(f"{Fore.MAGENTA}Checking {badge_name}...")
            
            try:
                method_name = badge_info["check_method"]
                if hasattr(self, method_name):
                    current_count = getattr(self, method_name)()
                else:
                    current_count = 0
                    
                # Determine tier achieved
                achieved_tier = None
                for tier, requirement in sorted(badge_info["tiers"].items(), 
                                              key=lambda x: x[1]):
                    if current_count >= requirement:
                        achieved_tier = tier
                        
                progress[badge_name] = {
                    "current": current_count,
                    "achieved_tier": achieved_tier,
                    "next_requirement": None,
                    "description": badge_info["description"],
                    "tiers": badge_info["tiers"]
                }
                
                # Find next requirement
                for tier, requirement in sorted(badge_info["tiers"].items(), 
                                              key=lambda x: x[1]):
                    if current_count < requirement:
                        progress[badge_name]["next_requirement"] = {
                            "tier": tier,
                            "count": requirement,
                            "needed": requirement - current_count
                        }
                        break
                        
            except Exception as e:
                print(f"{Fore.RED}Error checking {badge_name}: {e}")
                progress[badge_name] = {
                    "current": 0,
                    "achieved_tier": None,
                    "next_requirement": None,
                    "description": badge_info["description"],
                    "tiers": badge_info["tiers"],
                    "error": str(e)
                }
                
        return progress
        
    def generate_progress_report(self, progress: Dict) -> str:
        """Generate a formatted progress report"""
        
        report_lines = [
            f"{Fore.GREEN}🏆 GitHub Achievement Badge Progress Report",
            f"{Fore.CYAN}User: {self.user.login}",
            f"{Fore.CYAN}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        # Create table data
        table_data = []
        for badge_name, info in progress.items():
            current = info["current"]
            tier = info["achieved_tier"] or "None"
            
            if info.get("next_requirement"):
                next_req = f"{info['next_requirement']['tier']} ({info['next_requirement']['needed']} more)"
            else:
                next_req = "Max achieved!"
                
            # Status emoji
            if info["achieved_tier"]:
                if info["achieved_tier"] == "Gold":
                    status = "🥇"
                elif info["achieved_tier"] == "Silver":
                    status = "🥈"
                elif info["achieved_tier"] == "Bronze":
                    status = "🥉"
                else:
                    status = "✅"
            else:
                status = "❌"
                
            table_data.append([
                status,
                badge_name[:20],  # Truncate long names
                current,
                tier,
                next_req[:25]  # Truncate long requirements
            ])
            
        # Format table
        headers = ["Status", "Badge", "Current", "Tier", "Next Goal"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        report_lines.append(table)
        report_lines.append("")
        
        # Add detailed breakdown
        report_lines.append(f"{Fore.YELLOW}📊 Detailed Breakdown:")
        report_lines.append("")
        
        for badge_name, info in progress.items():
            if info.get("error"):
                report_lines.append(f"{Fore.RED}❌ {badge_name}: Error - {info['error']}")
                continue
                
            report_lines.append(f"{Fore.CYAN}🎯 {badge_name}")
            report_lines.append(f"   📝 {info['description']}")
            report_lines.append(f"   📊 Current: {info['current']}")
            
            if info["achieved_tier"]:
                report_lines.append(f"   🏆 Achieved: {info['achieved_tier']} tier")
            else:
                report_lines.append(f"   🎯 Not yet achieved")
                
            # Show tier requirements
            tier_info = []
            for tier, req in info["tiers"].items():
                status = "✅" if info["current"] >= req else "❌"
                tier_info.append(f"{status} {tier}: {req}")
            report_lines.append(f"   📈 Tiers: {' | '.join(tier_info)}")
            
            if info.get("next_requirement"):
                next_req = info["next_requirement"]
                report_lines.append(f"   🎯 Next: {next_req['tier']} tier ({next_req['needed']} more needed)")
                
            report_lines.append("")
            
        return "\n".join(report_lines)

@click.group()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.pass_context
def cli(ctx, token):
    """Badge Tracker for GitHub Achievement Badges"""
    if not token:
        print(f"{Fore.RED}Error: GitHub token is required. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
        
    ctx.ensure_object(dict)
    ctx.obj['tracker'] = BadgeTracker(token)

@cli.command()
@click.option('--output', type=click.Path(), help='Save report to file')
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.pass_context
def check(ctx, output, format):
    """Check current badge progress"""
    
    tracker = ctx.obj['tracker']
    
    print(f"{Fore.GREEN}🔍 Checking badge progress...")
    progress = tracker.get_badge_progress()
    
    if format == 'json':
        report = json.dumps(progress, indent=2, default=str)
    else:
        report = tracker.generate_progress_report(progress)
    
    if output:
        with open(output, 'w') as f:
            f.write(report)
        print(f"{Fore.GREEN}✅ Report saved to {output}")
    else:
        print(report)

@cli.command()
@click.pass_context
def summary(ctx):
    """Show a quick summary of badge status"""
    
    tracker = ctx.obj['tracker']
    progress = tracker.get_badge_progress()
    
    print(f"{Fore.GREEN}📊 Quick Badge Summary for {tracker.user.login}")
    print()
    
    achieved = 0
    total = len(progress)
    
    for badge_name, info in progress.items():
        if info["achieved_tier"]:
            achieved += 1
            tier_color = Fore.GREEN
            tier = info["achieved_tier"]
        else:
            tier_color = Fore.RED
            tier = "Not achieved"
            
        print(f"  {tier_color}{'✅' if info['achieved_tier'] else '❌'} {badge_name}: {tier}")
        
    print()
    print(f"{Fore.CYAN}Total Progress: {achieved}/{total} badges achieved ({achieved/total*100:.1f}%)")
    
    # Show next easiest targets
    next_targets = []
    for badge_name, info in progress.items():
        if info.get("next_requirement") and not info.get("error"):
            next_targets.append((
                badge_name,
                info["next_requirement"]["needed"],
                info["next_requirement"]["tier"]
            ))
            
    if next_targets:
        next_targets.sort(key=lambda x: x[1])  # Sort by needed count
        print(f"\n{Fore.YELLOW}🎯 Next Easiest Targets:")
        for badge, needed, tier in next_targets[:3]:
            print(f"  • {badge}: {needed} more for {tier} tier")

@cli.command()
@click.pass_context
def tips(ctx):
    """Show tips for earning specific badges"""
    
    tips_text = f"""
{Fore.GREEN}💡 Badge Earning Tips

{Fore.CYAN}🔥 Quick Wins (Easiest to achieve):
1. {Fore.MAGENTA}Heart On Your Sleeve: Just need 1 merged PR
   • Find good first issues in popular repos
   • Fix typos, improve documentation
   • Small, helpful contributions are best

2. {Fore.MAGENTA}Quickdraw: Close issue/PR within 5 minutes
   • Create an issue in your own repo
   • Wait 30 seconds, then close it
   • One-time achievement, very easy

3. {Fore.MAGENTA}YOLO: Merge PR without review
   • In your own repository, create and merge a PR
   • Don't request reviews before merging
   • One-time achievement

{Fore.CYAN}🚀 Medium Effort:
4. {Fore.MAGENTA}Pull Shark: Multiple merged PRs
   • Start with Heart On Your Sleeve
   • Continue contributing to different projects
   • Bronze (16) is achievable with consistent effort

5. {Fore.MAGENTA}Open Sourcerer: PRs in multiple repos
   • Contribute to 2-4 different repositories
   • Even small contributions count
   • Easier than Pull Shark numbers-wise

6. {Fore.MAGENTA}Pair Extraordinaire: Co-authored commits
   • Use co-author lines in commit messages
   • Work with dependabot or other contributors
   • Count merged PRs with co-authored commits

{Fore.CYAN}🎯 Long-term Goals:
7. {Fore.MAGENTA}Starstruck: Repository with many stars
   • Create useful open source projects
   • Share on social media, Reddit, HN
   • Default tier (16 stars) is achievable

8. {Fore.MAGENTA}Galaxy Brain: Answer discussions
   • Participate in GitHub Discussions
   • Provide helpful answers that get marked as solutions
   • Requires knowledge sharing

9. {Fore.MAGENTA}Public Sponsor: Sponsor someone
   • Use GitHub Sponsors to support developers
   • Even $1/month counts
   • Immediate achievement when you sponsor

{Fore.YELLOW}📈 Recommended Order:
1. Quickdraw (5 minutes)
2. YOLO (10 minutes)
3. Heart On Your Sleeve (1-7 days)
4. Open Sourcerer (1-2 weeks)
5. Pull Shark Bronze (1-2 months)
6. Pair Extraordinaire (1-2 months)
7. Starstruck (2-6 months)
8. Galaxy Brain (ongoing)
9. Public Sponsor (when financially comfortable)
"""
    
    print(tips_text)

if __name__ == "__main__":
    cli()
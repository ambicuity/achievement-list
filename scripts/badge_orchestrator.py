#!/usr/bin/env python3
"""
Badge Orchestrator - Comprehensive Badge Earning Automation

This script orchestrates the earning of all GitHub achievement badges
by coordinating existing tools and providing a systematic approach.
"""

import os
import sys
import time
import click
import json
from datetime import datetime, timedelta
from github import Github
from colorama import init, Fore, Style
from typing import List, Dict, Optional, Tuple
import subprocess

# Import existing tools
from badge_tracker import BadgeTracker

init(autoreset=True)

class BadgeOrchestrator:
    def __init__(self, token: str):
        self.github = Github(token)
        self.token = token
        self.user = self.github.get_user()
        self.tracker = BadgeTracker(token)
        
        # Badge earning order (easiest to hardest)
        self.earning_order = [
            "Quickdraw",           # 5 minutes - can be automated
            "YOLO",                # 10 minutes - can be automated  
            "Public Sponsor",      # 5 minutes - manual but easy
            "Heart On Your Sleeve", # 1-7 days - can be assisted
            "Open Sourcerer",      # 1-2 weeks - can be assisted
            "Pair Extraordinaire", # 1-2 months - can be assisted
            "Pull Shark",          # 2-6 months - builds on Heart On Your Sleeve
            "Galaxy Brain",        # 1-6 months - manual but can be guided
            "Starstruck"          # 2-12 months - long term manual goal
        ]
        
    def get_earning_plan(self) -> Dict:
        """Create a personalized badge earning plan"""
        
        print(f"{Fore.CYAN}🎯 Creating personalized badge earning plan...")
        progress = self.tracker.get_badge_progress()
        
        plan = {
            "immediate": [],     # Can be done right now (automated)
            "quick": [],         # Can be done in minutes/hours (semi-automated)
            "short_term": [],    # Days to weeks (guided)
            "long_term": [],     # Months (manual with guidance)
            "completed": []      # Already achieved
        }
        
        for badge_name in self.earning_order:
            if badge_name in progress:
                badge_info = progress[badge_name]
                
                if badge_info["achieved_tier"]:
                    plan["completed"].append({
                        "name": badge_name,
                        "tier": badge_info["achieved_tier"],
                        "description": badge_info["description"]
                    })
                else:
                    # Categorize based on difficulty and automation potential
                    if badge_name in ["Quickdraw", "YOLO"]:
                        plan["immediate"].append({
                            "name": badge_name,
                            "description": badge_info["description"],
                            "next_requirement": badge_info.get("next_requirement"),
                            "automated": True
                        })
                    elif badge_name in ["Public Sponsor"]:
                        plan["quick"].append({
                            "name": badge_name,
                            "description": badge_info["description"],
                            "next_requirement": badge_info.get("next_requirement"),
                            "automated": False,
                            "manual_steps": ["Go to GitHub Sponsors", "Sponsor any developer $1/month"]
                        })
                    elif badge_name in ["Heart On Your Sleeve", "Open Sourcerer", "Pair Extraordinaire"]:
                        plan["short_term"].append({
                            "name": badge_name,
                            "description": badge_info["description"],
                            "next_requirement": badge_info.get("next_requirement"),
                            "automated": False,
                            "tools_available": True
                        })
                    else:
                        plan["long_term"].append({
                            "name": badge_name,
                            "description": badge_info["description"],
                            "next_requirement": badge_info.get("next_requirement"),
                            "automated": False,
                            "tools_available": False
                        })
        
        return plan
        
    def execute_immediate_badges(self, plan: Dict) -> List[str]:
        """Execute badges that can be earned immediately through automation"""
        
        earned_badges = []
        
        for badge in plan["immediate"]:
            badge_name = badge["name"]
            
            print(f"\n{Fore.GREEN}🚀 Attempting to earn: {badge_name}")
            print(f"{Fore.YELLOW}Description: {badge['description']}")
            
            try:
                if badge_name == "Quickdraw":
                    success = self._earn_quickdraw_badge()
                elif badge_name == "YOLO":
                    success = self._earn_yolo_badge()
                else:
                    print(f"{Fore.YELLOW}⚠️  No automation available for {badge_name}")
                    continue
                    
                if success:
                    earned_badges.append(badge_name)
                    print(f"{Fore.GREEN}✅ Successfully earned {badge_name} badge!")
                else:
                    print(f"{Fore.RED}❌ Failed to earn {badge_name} badge")
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Error earning {badge_name}: {e}")
                
            # Wait between attempts to avoid rate limiting
            time.sleep(2)
            
        return earned_badges
        
    def _earn_quickdraw_badge(self) -> bool:
        """Attempt to earn Quickdraw badge"""
        
        print(f"{Fore.CYAN}  📝 Creating repository for Quickdraw badge...")
        
        try:
            # Create a temporary repository
            repo_name = f"quickdraw-{int(time.time())}"
            repo = self.user.create_repo(
                name=repo_name,
                description="Temporary repository for earning Quickdraw badge",
                private=False,
                auto_init=True
            )
            
            print(f"{Fore.GREEN}  ✅ Created repository: {repo.full_name}")
            
            # Create an issue
            issue_title = "Documentation improvement suggestion"
            issue_body = """## Summary
Quick documentation improvement that can be addressed immediately.

## Action
This issue will be closed as it's addressed by existing documentation.
"""
            
            print(f"{Fore.CYAN}  📝 Creating issue...")
            issue = repo.create_issue(title=issue_title, body=issue_body)
            print(f"{Fore.GREEN}  ✅ Issue created: {issue.number}")
            
            # Wait 30 seconds to ensure proper timing
            print(f"{Fore.YELLOW}  ⏳ Waiting 30 seconds before closing...")
            time.sleep(30)
            
            # Close the issue
            issue.edit(state="closed")
            print(f"{Fore.GREEN}  ✅ Issue closed within time limit!")
            
            # Clean up - delete the repository
            print(f"{Fore.CYAN}  🧹 Cleaning up temporary repository...")
            repo.delete()
            print(f"{Fore.GREEN}  ✅ Repository cleaned up")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}  ❌ Error in Quickdraw automation: {e}")
            # Try to clean up if repo was created
            try:
                if 'repo' in locals():
                    repo.delete()
            except:
                pass
            return False
            
    def _earn_yolo_badge(self) -> bool:
        """Attempt to earn YOLO badge"""
        
        print(f"{Fore.CYAN}  📝 Creating repository for YOLO badge...")
        
        try:
            # Create a temporary repository
            repo_name = f"yolo-badge-{int(time.time())}"
            repo = self.user.create_repo(
                name=repo_name,
                description="Temporary repository for earning YOLO badge",
                private=False,
                auto_init=True
            )
            
            print(f"{Fore.GREEN}  ✅ Created repository: {repo.full_name}")
            
            # Get the main branch
            main_branch = repo.get_branch("main")
            
            # Create a new file
            file_content = """# YOLO Badge Earning
            
This repository was created to earn the YOLO badge by merging a PR without review.

## Badge Requirements
- Merge a pull request without requesting or waiting for reviews
- This demonstrates confidence in your changes (hence "YOLO" - You Only Live Once)

## Implementation
This PR adds this README file to document the badge earning process.
"""
            
            # Create a new branch
            new_branch_name = "add-readme"
            new_branch = repo.create_git_ref(
                ref=f"refs/heads/{new_branch_name}",
                sha=main_branch.commit.sha
            )
            
            print(f"{Fore.GREEN}  ✅ Created branch: {new_branch_name}")
            
            # Create file in new branch
            repo.create_file(
                path="README.md",
                message="Add README for YOLO badge earning",
                content=file_content,
                branch=new_branch_name
            )
            
            print(f"{Fore.GREEN}  ✅ Created file in branch")
            
            # Create pull request
            pr = repo.create_pull(
                title="Add README for YOLO badge",
                body="Adding README file to document YOLO badge earning process.\n\nThis PR will be merged without review to earn the YOLO badge.",
                head=new_branch_name,
                base="main"
            )
            
            print(f"{Fore.GREEN}  ✅ Created PR: {pr.number}")
            
            # Merge immediately without review (YOLO!)
            merge_result = pr.merge(
                commit_message="Merge YOLO badge PR",
                merge_method="merge"
            )
            
            print(f"{Fore.GREEN}  ✅ PR merged without review - YOLO badge earned!")
            
            # Clean up - delete the repository
            print(f"{Fore.CYAN}  🧹 Cleaning up temporary repository...")
            repo.delete()
            print(f"{Fore.GREEN}  ✅ Repository cleaned up")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}  ❌ Error in YOLO automation: {e}")
            # Try to clean up if repo was created
            try:
                if 'repo' in locals():
                    repo.delete()
            except:
                pass
            return False
            
    def provide_guidance_for_remaining_badges(self, plan: Dict):
        """Provide detailed guidance for badges that require manual effort"""
        
        print(f"\n{Fore.CYAN}📋 Guidance for Remaining Badges")
        print("=" * 50)
        
        if plan["quick"]:
            print(f"\n{Fore.YELLOW}⚡ Quick Wins (Manual - 5-30 minutes):")
            for badge in plan["quick"]:
                print(f"\n  🎯 {badge['name']}")
                print(f"     📝 {badge['description']}")
                if "manual_steps" in badge:
                    for i, step in enumerate(badge["manual_steps"], 1):
                        print(f"     {i}. {step}")
                        
        if plan["short_term"]:
            print(f"\n{Fore.GREEN}📈 Short-term Goals (Tool-assisted - Days to weeks):")
            for badge in plan["short_term"]:
                print(f"\n  🎯 {badge['name']}")
                print(f"     📝 {badge['description']}")
                if badge.get("next_requirement"):
                    req = badge["next_requirement"]
                    print(f"     🎯 Next: {req['tier']} tier ({req['needed']} more needed)")
                    
                # Provide tool suggestions
                if badge["name"] == "Heart On Your Sleeve":
                    print(f"     🛠️  Use: python scripts/badge_cli.py find-repos")
                elif badge["name"] == "Open Sourcerer":
                    print(f"     🛠️  Use: python scripts/badge_cli.py find-repos --language <your_language>")
                elif badge["name"] == "Pair Extraordinaire":
                    print(f"     🛠️  Use: python scripts/badge_cli.py coauthor")
                    
        if plan["long_term"]:
            print(f"\n{Fore.MAGENTA}🏔️  Long-term Goals (Manual - Months):")
            for badge in plan["long_term"]:
                print(f"\n  🎯 {badge['name']}")
                print(f"     📝 {badge['description']}")
                if badge.get("next_requirement"):
                    req = badge["next_requirement"]
                    print(f"     🎯 Next: {req['tier']} tier ({req['needed']} more needed)")
                    
                # Provide strategy suggestions
                if badge["name"] == "Starstruck":
                    print(f"     💡 Strategy: Create useful open source projects")
                elif badge["name"] == "Galaxy Brain":
                    print(f"     💡 Strategy: Answer GitHub Discussions")
                elif badge["name"] == "Pull Shark":
                    print(f"     💡 Strategy: Continue contributing (builds on Heart On Your Sleeve)")
                    
    def verify_badge_progress(self) -> Dict:
        """Verify current badge progress after earning attempts"""
        
        print(f"\n{Fore.CYAN}🔍 Verifying badge progress...")
        
        # Wait a moment for GitHub to process
        time.sleep(5)
        
        # Get fresh progress data
        progress = self.tracker.get_badge_progress()
        
        # Count achievements
        earned_count = sum(1 for badge in progress.values() if badge["achieved_tier"])
        total_count = len(progress)
        
        print(f"\n{Fore.GREEN}📊 Badge Progress Summary:")
        print(f"   🏆 Badges earned: {earned_count}/{total_count}")
        print(f"   📈 Completion: {earned_count/total_count*100:.1f}%")
        
        return progress

@click.group()
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.pass_context
def cli(ctx, token):
    """Badge Orchestrator - Comprehensive Badge Earning Automation"""
    if not token:
        print(f"{Fore.RED}❌ GitHub token required. Set GITHUB_TOKEN environment variable or use --token")
        print(f"{Fore.YELLOW}⚠️  Security Note: Never commit tokens to repositories!")
        sys.exit(1)
        
    ctx.ensure_object(dict)
    ctx.obj['orchestrator'] = BadgeOrchestrator(token)

@cli.command()
@click.option('--execute', is_flag=True, help='Execute automated badge earning (not just plan)')
@click.option('--verify', is_flag=True, help='Verify badge progress after execution')
@click.pass_context
def earn_all(ctx, execute, verify):
    """Create and optionally execute a comprehensive badge earning plan"""
    
    orchestrator = ctx.obj['orchestrator']
    
    print(f"{Fore.GREEN}🏆 GitHub Achievement Badge Orchestrator")
    print(f"{Fore.CYAN}User: {orchestrator.user.login}")
    print(f"{Fore.CYAN}Mode: {'Execute + Plan' if execute else 'Plan Only'}")
    print("=" * 60)
    
    # Get personalized earning plan
    plan = orchestrator.get_earning_plan()
    
    # Show current progress
    if plan["completed"]:
        print(f"\n{Fore.GREEN}✅ Already Earned ({len(plan['completed'])}):")
        for badge in plan["completed"]:
            print(f"   🏆 {badge['name']} ({badge['tier']} tier)")
    
    # Show what can be earned immediately
    if plan["immediate"]:
        print(f"\n{Fore.CYAN}🚀 Available for Immediate Earning ({len(plan['immediate'])}):")
        for badge in plan["immediate"]:
            print(f"   ⚡ {badge['name']} - {badge['description']}")
            
        if execute:
            print(f"\n{Fore.YELLOW}🎯 Executing immediate badge earning...")
            earned = orchestrator.execute_immediate_badges(plan)
            
            if earned:
                print(f"\n{Fore.GREEN}🎉 Successfully earned {len(earned)} badge(s): {', '.join(earned)}")
            else:
                print(f"\n{Fore.YELLOW}⚠️  No badges were automatically earned (may require manual verification)")
        else:
            print(f"\n{Fore.YELLOW}💡 Run with --execute flag to automatically earn these badges")
    
    # Provide guidance for remaining badges
    orchestrator.provide_guidance_for_remaining_badges(plan)
    
    # Verify progress if requested
    if verify:
        final_progress = orchestrator.verify_badge_progress()
    
    # Show next steps
    print(f"\n{Fore.GREEN}🎯 Next Steps:")
    print(f"   1. Run: python scripts/badge_cli.py status  # Check current progress")
    print(f"   2. Follow the guidance above for remaining badges")
    print(f"   3. Use: python scripts/badge_cli.py dashboard  # View your achievements")
    print(f"   4. Re-run this command periodically to track progress")

@cli.command()
@click.pass_context
def plan(ctx):
    """Show badge earning plan without execution"""
    ctx.invoke(earn_all, execute=False, verify=False)

@cli.command()
@click.pass_context
def execute(ctx):
    """Execute automated badge earning with verification"""
    ctx.invoke(earn_all, execute=True, verify=True)

if __name__ == "__main__":
    cli()
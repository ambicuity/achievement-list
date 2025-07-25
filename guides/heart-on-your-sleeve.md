# Heart On Your Sleeve Badge Guide

**Badge Requirement:** Submit a pull request that gets merged.

**Difficulty:** ⭐⭐ (Easy-Medium)  
**Time to Achieve:** 1-7 days  
**Tiers:** Default (1), Bronze (2), Silver (4), Gold (8)

## Overview

The Heart On Your Sleeve badge is earned by getting pull requests merged. This is often the first "real" contribution badge developers earn and serves as a gateway to open source contribution.

## Quick Start Strategy

### Step 1: Find Beginner-Friendly Repositories

Use the automation script:
```bash
export GITHUB_TOKEN="your_token_here"
python scripts/pr_automation.py --language python --min-stars 50
```

Or manually search for:
- Repositories with "good first issue" labels
- Documentation-heavy projects
- Projects you use regularly
- Newer projects seeking contributors

### Step 2: Types of Contributions (Easiest First)

#### 🥇 Documentation Improvements (Highest Success Rate)
- **Fix typos and grammar** in README files
- **Improve code examples** that don't work
- **Add missing installation steps**
- **Clarify confusing explanations**
- **Fix broken links**

#### 🥈 Code Quality Improvements  
- **Add missing comments** to complex code
- **Fix code formatting** inconsistencies
- **Update deprecated function calls**
- **Add error handling** where missing

#### 🥉 Small Feature Additions
- **Add configuration options**
- **Improve error messages**
- **Add simple utility functions**
- **Enhance CLI help text**

## Contribution Process

### 1. Repository Research
```bash
# Find suitable repositories
python scripts/pr_automation.py --interactive

# Check if you can contribute
- Look for CONTRIBUTING.md
- Check recent PR activity
- Read issue guidelines
- Verify license compatibility
```

### 2. Issue Selection
- Start with issues labeled `good first issue`
- Look for `help wanted` labels
- Choose issues with clear descriptions
- Avoid complex or controversial topics

### 3. Making Your Contribution

#### Documentation PR Example:
```bash
# 1. Fork and clone
git clone https://github.com/your-username/target-repo.git
cd target-repo

# 2. Create branch
git checkout -b improve/readme-clarity

# 3. Make changes
# Edit README.md to fix typos, improve examples

# 4. Commit with clear message
git add README.md
git commit -m "docs: fix typos and improve installation examples

- Corrected spelling errors in installation section
- Updated outdated command examples  
- Added clarity to troubleshooting steps"

# 5. Push and create PR
git push origin improve/readme-clarity
# Then create PR via GitHub web interface
```

## PR Best Practices

### Title Format
- Use conventional commits: `docs:`, `fix:`, `feat:`
- Be specific and clear
- Example: `docs: fix typos in installation guide`

### Description Template
```markdown
## Summary
Brief description of what this PR does.

## Changes
- Specific change 1
- Specific change 2  
- Specific change 3

## Testing
- [ ] Documentation builds without errors
- [ ] All links work correctly
- [ ] Examples are tested and functional

## Screenshots (if applicable)
Before/after screenshots for UI changes.
```

### Code Quality
- Follow the project's style guide
- Test your changes thoroughly
- Keep changes focused and minimal
- Add appropriate comments

## Repository Recommendations

### Beginner-Friendly Projects
- **Documentation sites** (Gatsby, Jekyll themes)
- **CLI tools** (often need help text improvements)
- **Tutorial repositories** (examples often break)
- **Awesome lists** (easy additions)

### Search Strategies
```bash
# GitHub search queries
is:public archived:false good-first-issue language:python stars:>100
is:public archived:false help-wanted language:javascript stars:>50
is:public archived:false documentation language:markdown stars:>20
```

## Common Pitfalls

### ❌ Avoid These Mistakes
- **Large, complex changes** as first contributions
- **Controversial or opinionated changes**
- **Breaking changes** without discussion
- **Poor commit messages** or descriptions
- **Not reading contribution guidelines**

### ✅ Success Factors
- **Small, focused changes** are more likely to be merged
- **Clear communication** with maintainers
- **Following project conventions**
- **Being responsive** to feedback
- **Testing changes** thoroughly

## Tracking Progress

### Using Badge Tracker
```bash
# Check current progress
python scripts/badge_tracker.py check

# Get quick summary
python scripts/badge_tracker.py summary
```

### Manual Verification
1. Check your GitHub profile for merged PRs
2. Search: `type:pr author:your-username is:merged`
3. Badge appears in GitHub profile achievements

## Tier Progression

| Tier | Requirement | Strategy |
|------|-------------|----------|
| Default | 1 merged PR | Focus on one good documentation fix |
| Bronze | 2 merged PRs | Add one more small contribution |
| Silver | 4 merged PRs | Regular contributions over a month |
| Gold | 8 merged PRs | Consistent contributor pattern |

## Time Investment

- **Research:** 30-60 minutes to find good repositories
- **First PR:** 1-3 hours including learning process
- **Follow-up PRs:** 30-60 minutes each
- **Total for Default:** 2-4 hours over 1-7 days

## Advanced Tips

### Building Relationships
- **Comment on issues** before working on them
- **Join project communities** (Discord, forums)
- **Attend project meetings** if they're public
- **Help other contributors** in discussions

### Scaling Up
- **Become a regular contributor** to 2-3 projects
- **Mentor other new contributors**
- **Help with issue triage and code reviews**
- **Eventually become a maintainer**

## Troubleshooting

**PR not getting reviewed?**
- Check if maintainers are active
- Comment politely asking for review
- Join project chat for faster response
- Consider smaller, simpler changes

**PR rejected?**
- Don't take it personally
- Ask for specific feedback
- Learn from the experience
- Try a different approach or project

**Can't find good issues?**
- Create your own by reporting bugs
- Suggest improvements in discussions
- Look at recently updated repositories
- Check dependency update PRs for inspiration

The Heart On Your Sleeve badge is your gateway to open source contribution and leads naturally to other badges like Pull Shark and Open Sourcerer!
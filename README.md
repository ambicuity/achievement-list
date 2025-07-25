# 🏆 GitHub Achievement Badge Automation

Comprehensive tools and workflows to help you earn GitHub achievement badges as fast as possible!

## 🚀 Quick Start

```bash
# 1. Set up your GitHub token
export GITHUB_TOKEN="your_github_token_here"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Check your current progress
python scripts/badge_cli.py status

# 4. Get personalized tips
python scripts/badge_cli.py tips
```

## 🎯 Target Badges

| Badge | Difficulty | Time | Strategy |
|-------|------------|------|----------|
| [Quickdraw](guides/quickdraw.md) | ⭐ | 5 min | Close issue/PR within 5 minutes |
| YOLO | ⭐ | 10 min | Merge PR without review |
| [Heart On Your Sleeve](guides/heart-on-your-sleeve.md) | ⭐⭐ | 1-7 days | First merged PR |
| Public Sponsor | ⭐⭐ | 5 min | Sponsor someone $1/month |
| Open Sourcerer | ⭐⭐ | 1-2 weeks | PRs in multiple repos |
| Pair Extraordinaire | ⭐⭐⭐ | 1-2 months | Co-authored commits |
| Pull Shark | ⭐⭐⭐ | 2-6 months | Many merged PRs |
| Starstruck | ⭐⭐⭐⭐ | 2-12 months | Popular repository |
| Galaxy Brain | ⭐⭐⭐⭐ | 1-6 months | Answer discussions |

## 🛠️ Tools & Scripts

### Main CLI Tool
```bash
python scripts/badge_cli.py --help      # See all commands
python scripts/badge_cli.py status      # Check badge progress
python scripts/badge_cli.py quickdraw   # Earn Quickdraw badge
python scripts/badge_cli.py find-repos  # Find contribution opportunities
```

### Individual Tools
- **`pr_automation.py`** - Find repositories and automate PR workflows
- **`quickdraw_automation.py`** - Achieve Quickdraw badge in 5 minutes
- **`coauthor_helper.py`** - Generate co-authored commits for Pair Extraordinaire
- **`discussion_finder.py`** - Find GitHub discussions for Galaxy Brain badge
- **`badge_tracker.py`** - Track your progress across all badges

### GitHub Actions Workflows
- **Badge Progress Tracker** - Weekly automated progress reports
- **Quickdraw PR Automation** - Automated PR creation and closure

## 📊 Badge Requirements

### Heart On Your Sleeve
**Requirement:** Submit a pull request that gets merged
- Default: 1 | Bronze: 2 | Silver: 4 | Gold: 8

### Open Sourcerer  
**Requirement:** User had PRs merged in multiple public repositories
- Default: 1 | Bronze: 2 | Silver: 3 | Gold: 4

### Starstruck
**Requirement:** Created a repository that has many stars
- Default: 16 | Bronze: 128 | Silver: 512 | Gold: 4096

### Quickdraw
**Requirement:** Closed an issue/pull request within 5 minutes of opening
- Default: 1

### Pair Extraordinaire
**Requirement:** Coauthored commits on merged pull request  
- Default: 1 | Bronze: 10 | Silver: 24 | Gold: 48

### Pull Shark
**Requirement:** Opened a pull request that has been merged
- Default: 2 | Bronze: 16 | Silver: 128 | Gold: 1024

### Galaxy Brain
**Requirement:** Answered a discussion (got an accepted answer)
- Default: 2 | Bronze: 8 | Silver: 16 | Gold: 32

### YOLO
**Requirement:** Merged a pull request without a review
- Default: 1

### Public Sponsor
**Requirement:** Sponsored an open source contributor through GitHub Sponsors
- Default: 1

## 📚 Comprehensive Guides

Detailed guides for each badge are available in the [`guides/`](guides/) directory:

- [Heart On Your Sleeve Guide](guides/heart-on-your-sleeve.md) - Your first merged PR
- [Quickdraw Guide](guides/quickdraw.md) - 5-minute achievement
- [Complete Guide Index](guides/README.md) - All guides and strategies

## ⚡ Fastest Path to Badges

### 5-Minute Achievements
1. **Quickdraw** - `python scripts/badge_cli.py quickdraw`
2. **YOLO** - Create and merge PR in your own repo without review
3. **Public Sponsor** - Sponsor any developer $1/month via GitHub Sponsors

### Week 1-2 Goals  
4. **Heart On Your Sleeve** - Make your first contribution
5. **Open Sourcerer** - Contribute to 2+ different repositories

### Month 1-3 Goals
6. **Pull Shark Bronze** - 16 merged PRs
7. **Pair Extraordinaire** - 10 co-authored commits

### Long-term Goals
8. **Starstruck** - Build something people star
9. **Galaxy Brain** - Help others in discussions

## 🔧 Setup

### Prerequisites
- GitHub account
- GitHub Personal Access Token with `repo` scope
- Python 3.8+

### Installation
```bash
# Clone this repository
git clone https://github.com/ambicuity/achievement-list.git
cd achievement-list

# Install dependencies
pip install -r requirements.txt

# Set up GitHub token
export GITHUB_TOKEN="your_token_here"
# Add to your .bashrc/.zshrc for persistence

# Verify setup
python scripts/badge_cli.py setup
```

### GitHub Token Setup
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`, `read:org`
4. Copy the token and set it as an environment variable

## 🤖 Automation Features

- **Repository Discovery** - Find beginner-friendly projects
- **PR Template Generation** - Create effective pull request descriptions
- **Progress Tracking** - Monitor badge advancement
- **Quickdraw Automation** - Earn badges in minutes
- **Co-author Management** - Generate proper co-author commit messages
- **Discussion Finding** - Locate opportunities for Galaxy Brain badge

## 📈 Progress Tracking

```bash
# Quick status check
python scripts/badge_tracker.py summary

# Detailed progress report  
python scripts/badge_tracker.py check

# Export progress data
python scripts/badge_tracker.py check --output progress.json --format json
```

## 🏗️ GitHub Actions Integration

### Badge Progress Tracker
Automatically tracks your badge progress weekly:

```yaml
# Runs every Monday at noon UTC
- cron: '0 12 * * 1'
```

### Quickdraw Automation
On-demand workflow to earn Quickdraw badge:

```bash
# Trigger via GitHub Actions tab
# Creates PR, waits 60 seconds, then closes it
```

## 🎯 Best Practices

### Ethical Guidelines
- Make genuine, helpful contributions
- Respect repository maintainers and communities  
- Follow each project's contribution guidelines
- Don't spam or create low-quality content
- Be patient and respectful in all interactions

### Contribution Tips
- Start with documentation improvements
- Fix typos and broken links
- Add missing examples or clarifications
- Focus on projects you actually use
- Build relationships with maintainers

## 🤝 Contributing

We welcome contributions to improve these automation tools!

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star This Repository

If these tools help you earn badges, please star this repository to help others discover it!

---

**Disclaimer:** These tools are designed to help you earn badges through legitimate contributions and activities. Always follow GitHub's Terms of Service and community guidelines.


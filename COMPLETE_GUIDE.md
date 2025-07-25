# Complete Badge Earning Guide

## Quick Setup

1. **Get your GitHub Personal Access Token**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `read:user`, `read:org`
   - Copy the token (keep it secure!)

2. **Set up environment** (IMPORTANT - keep token secure):
   ```bash
   # Method 1: Environment variable (recommended)
   export GITHUB_TOKEN="your_token_here"
   
   # Method 2: Using .env file
   cp .env.example .env
   # Edit .env and add your token (file is gitignored)
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Earn All Badges Automatically

### One-Command Solution
```bash
# See your personalized badge earning plan
python scripts/badge_cli.py earn plan

# Execute automated badge earning (safe - only automates Quickdraw and YOLO)
python scripts/badge_cli.py earn execute

# Complete automation with verification
python scripts/badge_cli.py earn all --execute --verify
```

### What Gets Automated
- ✅ **Quickdraw badge**: Creates temporary repo, opens issue, closes it within 5 minutes
- ✅ **YOLO badge**: Creates temporary repo, makes PR, merges without review
- ❓ **Other badges**: Provides detailed guidance and tool suggestions

### What Requires Manual Action
- **Public Sponsor**: Go to GitHub Sponsors, sponsor someone $1/month
- **Heart On Your Sleeve**: Use `badge find-repos` to find contribution opportunities
- **Open Sourcerer**: Contribute to multiple repositories
- **Pair Extraordinaire**: Use `badge coauthor` for co-authored commits
- **Pull Shark**: Build on Heart On Your Sleeve contributions
- **Galaxy Brain**: Answer GitHub Discussions
- **Starstruck**: Create popular open source projects

## Security Best Practices

🔒 **NEVER commit your GitHub token to any repository!**

- Use environment variables or .env files (which are gitignored)
- Rotate your tokens regularly
- Use minimal required scopes
- Keep tokens private and secure

## Progress Tracking

```bash
# Check current badge status
python scripts/badge_cli.py status

# Get personalized tips
python scripts/badge_cli.py tips

# View badges in browser
python scripts/badge_cli.py dashboard
```

## Estimated Timeline

- **Immediate (5-10 minutes)**: Quickdraw, YOLO
- **Quick wins (30 minutes)**: Public Sponsor
- **Short term (1-4 weeks)**: Heart On Your Sleeve, Open Sourcerer
- **Medium term (1-6 months)**: Pair Extraordinaire, Pull Shark, Galaxy Brain
- **Long term (6+ months)**: Starstruck

## Troubleshooting

### "GitHub token required"
- Make sure `GITHUB_TOKEN` environment variable is set
- Run `python scripts/badge_cli.py setup` to verify configuration

### "Permission denied" errors
- Check your token has correct scopes: `repo`, `read:user`, `read:org`
- Regenerate token if needed

### Badge not showing immediately
- GitHub badges can take 24-48 hours to appear
- Use `python scripts/badge_cli.py status` to verify automated actions worked
- Some badges require manual verification on GitHub's side

### Rate limiting
- The automation includes delays to avoid rate limits
- If you hit limits, wait an hour and try again
- Temporary repositories are automatically cleaned up
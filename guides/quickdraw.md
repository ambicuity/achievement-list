# Quickdraw Badge Guide

**Badge Requirement:** Close an issue or pull request within 5 minutes of opening it.

**Difficulty:** ⭐ (Very Easy)  
**Time to Achieve:** 5 minutes  
**Tiers:** Default only (1 achievement)

## Overview

The Quickdraw badge is one of the easiest GitHub achievements to earn. You simply need to close an issue or pull request within 5 minutes of creating it. This is a one-time achievement with no tiers.

## Strategy 1: Quick Issue (Recommended)

### Manual Method

1. **Go to any repository you own** (or have admin access to)
2. **Create a new issue** with a simple title like "Documentation improvement suggestion"
3. **Add a brief description** explaining it's a quick note
4. **Wait 30-60 seconds** (to avoid appearing too automated)
5. **Close the issue** with a comment like "Implemented in upcoming changes"

### Automated Method

Use the quickdraw automation script:

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_token_here"

# Run the quickdraw automation
python scripts/quickdraw_automation.py quick-issue --repo your-username/your-repo
```

## Strategy 2: Quick Pull Request

### Manual Method

1. **Clone one of your repositories**
   ```bash
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Create a branch and make a simple change**
   ```bash
   git checkout -b quickdraw/test
   echo "<!-- Quick update -->" >> README.md
   git add README.md
   git commit -m "docs: quick documentation note"
   git push origin quickdraw/test
   ```

3. **Create PR via GitHub web interface**
4. **Immediately close the PR** with a comment

### GitHub Actions Method

Use the automated workflow:

1. Go to your repository's Actions tab
2. Run the "Auto PR for Quickdraw Badge" workflow
3. The workflow will automatically create and close a PR

## Strategy 3: Monitor Existing Activity

If you have recent issues or PRs (created within the last few minutes):

```bash
# Check for recent activity
python scripts/quickdraw_automation.py monitor
```

## Important Notes

### Timing Requirements
- Must close within **5 minutes** of creation
- The timer starts when the issue/PR is created
- GitHub tracks this automatically

### What Counts
- ✅ Issues you created and closed
- ✅ Pull requests you created and closed
- ❌ Issues/PRs created by others (even if you close them)

### Best Practices
- Use your own repositories to avoid spam
- Add meaningful closing comments
- Don't create multiple issues just for the badge
- Make the issue/PR contextually reasonable

## Common Mistakes

1. **Closing too quickly** - Wait at least 30 seconds to appear natural
2. **Using other people's repos** - Only works with issues/PRs you created
3. **Not adding context** - Add a brief closing comment explaining why
4. **Creating spam** - Make issues that make sense in context

## Verification

After closing an issue/PR within 5 minutes:

1. **Check your GitHub profile** - Badges may take a few hours to appear
2. **Look for the Quickdraw badge** in your achievement section
3. **No tiers to worry about** - This is a one-time achievement

## Example Issue Template

**Title:** "Documentation clarity improvement suggestion"

**Body:**
```markdown
## Suggestion
Quick note about improving documentation clarity in the getting started section.

## Action
Closing this issue as it will be addressed in the next documentation update cycle.
```

**Closing Comment:**
```markdown
Closing this issue as the suggestion will be implemented in upcoming documentation improvements. Thanks for the feedback!
```

## Troubleshooting

**Badge not appearing?**
- Wait 24 hours - badges can be delayed
- Make sure you closed within 5 minutes
- Verify you created (not just closed) the issue/PR

**Don't have a repository?**
- Create a simple repository first
- Even a basic README-only repo works
- Use it for testing automation tools

## Time Investment

- **Setup:** 2 minutes (if you have a repo)
- **Execution:** 1-2 minutes
- **Total:** ~5 minutes for a guaranteed badge

This is the fastest GitHub achievement badge to earn and a great way to start your badge collection!
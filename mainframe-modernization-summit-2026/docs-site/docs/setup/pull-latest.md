# Pulling the latest changes

The workshop repo is updated frequently. **Before every session**, pull the latest version to make sure you have all the current challenges, fixes, and docs.

---

## GitHub Desktop (recommended)

### 1. Open the repo

Open **GitHub Desktop**. If the workshop repo isn't selected, click the **Current Repository** dropdown (top left) and select it.


### 2. Fetch from remote

Click the **Fetch origin** button in the top bar. This checks whether there are new commits on the remote.


### 3. Pull

If new commits are available, the button changes to **Pull origin**. Click it to download and apply the changes.

!!! success "You're up to date"
    When the button reads **Fetch origin** again (no number badge), your local copy matches the remote.

---

## Command line (alternative)

If you prefer the terminal, open it in the repo folder and run:

```bash
git pull
```

That's it — same result.

---

## Troubleshooting

### "You have local changes that would be overwritten"

This means you modified a file that was also updated upstream.

**Quick fix — stash and pull:**

```bash
git stash
git pull
git stash pop
```

If there's a conflict after `git stash pop`, open the file in VS Code — it will highlight the conflicting sections. Resolve them, save, and you're good.

### GitHub Desktop shows merge conflicts

1. GitHub Desktop will list the conflicting files.
2. Click **Open in Visual Studio Code** for each file.
3. VS Code highlights the conflicts — pick the version you want (usually **Accept Incoming Change**).
4. Save the file, go back to GitHub Desktop, and click **Continue Merge**.

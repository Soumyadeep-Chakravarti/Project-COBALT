---
title: "Log 0x9: The Great GitHub Actions Debacle"
date: 2026-04-11
categories: ["DevOps", "Documentation"]
tags: ["github-actions", "deployment", "astro", "github-pages"]
mermaid: false
---

# [ COBALT Engineering Log 0x9 ]
## The Great GitHub Actions Debacle

*April 11, 2026. 2:47 AM. Fourteen deploy attempts. Seven energy drinks. One working config.*

---

## The Problem ⚡

GitHub Actions kept failing with:

```
[LegacyContentConfigError] Found legacy content config file in "docs/src/content/config.ts". 
Please move this file to "src/content.config.ts" and ensure each collection has a loader defined.
```

AND ON THE DEPLOY SIDE:

```
[LegacyContentConfigError] Found legacy content config file in "docs/src/content/config.ts"
...
/node_modules
EntryFilter: excluded /node_modules
```

WHAT THE ACTUAL F***.

GH Pages was trying to run **Jekyll** on an Astro project. 

Let me say that again so it sinks in:

JEYKLL. ON ASTRO. ON MY BLOGS.

It's 2 in the morning and Jekyll is trying to process my Astro config like it's some kinda markdown blog from 2012. I haven't used Jekyll since I thought `git commit` was a magic spell. This thing died in a cave somewhere and GitHub dug it up and said "here, this is what we're running now, good luck"

---

## Why This Happened 🔥

| What GH Pages Sees | What It Does |
|-------------------|--------------|
| `docs/` folder | Runs Jekyll by default |
| `index.md` | Treats as Jekyll post |
| Any `config` | Tries to process as Jekyll config |

GH Pages defaults to Jekyll for **anything** in `docs/`.

This is like showing up to a cyberpunk bar in 2026 and they're like "sorry sir we only have mead, that's what we serve here, always has been"

THE YEAR IS 2026 GH Pages. WE HAVE ROCKETS ON MARS. WE HAVE AI WRITING CODE. AND YOU'RE RUNNING JYKL ON MY BLOG??

---

## The Solution 🚀

### 1. Disable Jekyll

```bash
touch docs/.nojekyll
```

Yeah that's right. Create an empty file that says "NOPE" to Jekyll. Sometimes the solution is just screaming NO at your tools until they listen.

### 2. Use Astro's build output (not docs/)

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install
        run: npm ci
      - name: Build
        run: npm run build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist  # <-- THE ONLY LINE THAT MATTERS
```

THAT LINE. `publish_dir: ./dist`. 

That's the line that says "deploy what i built, not where i wrote it". That's the line that saves careers. That's the line I've been screaming at my screen for three hours trying to find.

### 3. Point GH Pages to `/dist`

In GitHub repo settings:
- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/dist`

---

## The Architecture Before vs After

**BEFORE (the madness):**
```
.github/workflows/ 
  → builds 
  → tries to deploy docs/ 
  → Jekyll sees config files 
  → JYLL IS LIKE "ooh shiny" 
  → CHOKES 
  → DEPLOY FAILS 
  → WHY 
  → WHY GOD WHY
```

**AFTER (sweet sweet victory):**
```
.github/workflows/ 
  → builds 
  → deploys dist/ 
  → pages sees html 
  → pages goes "yep that's html" 
  → deploys 
  → WORKS
```

---

## The GitHub Actions Config That Works

```yaml
name: Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          
      - name: Install deps
        run: npm ci
        
      - name: Build Astro
        run: npm run build
        env:
          SITE_URL: 'https://cobalt.engineering'
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

This config took 14 tries to get right. 14. I've seen people get married and divorced faster than this deploy took to work.

---

## Key Takeaways 🎯

1. **GH Pages defaults to Jekyll** - It lives in 2008, refuses to leave, and will ruin your night if you don't fight it.

2. **Build locally, deploy output** - Build what you want to show, deploy what you built. Not your source. Never your source.

3. **`publish_dir: ./dist`** - This line is the difference between "nice website" and "why am i doing this with my life"

4. **`.nojekyll`** - A tiny file with massive power. It's a "leave me alone" sign for the digital dinosaur.

---

## Status

Deployment: Fixed ✅  
GH Actions: Configured ✅  
Sanity: 💀→🔪→✅ (it came back briefly)  

I am typing this at 3 AM having solved a problem that shouldn't exist in 2026. Jekyll shouldn't exist. Jekyll is a fossil. Jekyll is what happens when software gets ancient and nobody has the heart to put it down.

**The lesson: Always point to the build output, not the source. And maybe don't trust GitHub's defaults. They live in the past.**

---

*Previous: [Log 0x08: Nexus Resurfaces](/logs/0x8-nexus-resurface)*
# Implementation Guide: CLAUDE.md + PERSONAS.md System

This guide explains how to properly implement the CLAUDE.md and PERSONAS.md system across your projects, and what YOU (the human) need to do to make it work.

---

## What These Files Do

### CLAUDE.md
**Purpose:** Instructions for how I (Claude) should behave when working on your project.

- **GATE CHECK** — Forces me to think before coding
- **Hard Rules** — Non-negotiable constraints I must follow
- **Trigger Words** — Commands you can give me
- **Red Team** — Forces security review
- **Ship Checklist** — Quality gates before deployment

### PERSONAS.md
**Purpose:** Different "expert hats" I put on to evaluate decisions.

- **Named Personas** — Each with specific expertise
- **Veto Power** — Who can block what
- **Scoring** — Quantitative evaluation
- **Iteration Requirement** — Forces me to improve until good enough

---

## How to Set It Up

### Step 1: Place Files in Project Root

```
your-project/
├── CLAUDE.md          ← Project-specific rules
├── PERSONAS.md        ← Expert evaluation model
├── src/
├── package.json
└── ...
```

**The files MUST be in the project root.** This is where Claude Code and similar tools look for them.

### Step 2: Customize for Your Project

Don't just copy the templates — customize them:

1. **CLAUDE.md:**
   - Add your project's specific GATE CHECK items
   - Add domain-specific hard rules
   - Add your own trigger words
   - Fill in the Change Impact Checklist
   - Document your project context

2. **PERSONAS.md:**
   - Keep Security Engineer (always needed)
   - Add your domain expert (Math, Medical, Financial, etc.)
   - Add personas relevant to your project
   - Remove personas that don't apply

### Step 3: Commit to Git

```bash
git add CLAUDE.md PERSONAS.md
git commit -m "Add Claude behavioral guidelines and personas"
```

**Important:** These files should be version controlled so they evolve with your project.

---

## What YOU Need to Do

### 1. Start Conversations with Context

When you start a new conversation about a project, tell me to read the files:

> "Read CLAUDE.md and PERSONAS.md first."

Or, better yet, just have them in your project root and I'll read them when I see the codebase.

### 2. Use the Trigger Words

The trigger words are your controls. Use them:

| When You Want | Say |
|---------------|-----|
| Deploy to production | **"deploy"** |
| Full security review | **"audit"** or **"red team"** |
| Check against all personas | **"ask personas"** |
| Make sure I'm on track | **"spiral"** |
| Remind me of the rules | **"gate"** |
| Review payment code | **"payment check"** |

### 3. Enforce the Gates

If I skip the GATE CHECK, call me out:

> "You didn't do the gate check. Do it now."

The system only works if you enforce it. I might forget or rush — you're the enforcer.

### 4. Demand Iteration

If I present a first draft, push back:

> "Score this against the personas. If anything is below threshold, iterate."

Don't accept "good enough." The personas system forces quality — use it.

### 5. Question My Assumptions

The GATE CHECK makes me state my assumptions. Challenge them:

> "You said auth required: no. Why? This endpoint has user data."

I'll either correct myself or explain why I'm right.

---

## Enforcing Quality: Your Checklist

### Before Approving Any Code Change

Ask yourself:

- [ ] Did Claude do the GATE CHECK?
- [ ] Did Claude do domain-specific gates (PAYMENT GATE, etc.)?
- [ ] Did Claude red team security-relevant code?
- [ ] Did Claude state which tests are needed?
- [ ] Did Claude check for existing code first?

If NO to any: **Send it back.**

### Before Deploying

Ask yourself:

- [ ] Did Claude run the Ship Checklist?
- [ ] Did the build pass?
- [ ] Did tests pass?
- [ ] Were critical flows tested manually?
- [ ] Can we rollback if needed?

If NO to any: **Don't deploy.**

### When Tests Fail

**Never let me "fix" a test to make it pass without analysis.**

Demand the POST-TEST GATE:

> "The test failed. Do the POST-TEST GATE analysis before changing anything."

Default assumption: The implementation is wrong, not the test.

---

## Common Scenarios

### Scenario 1: Starting New Feature

**You say:** "I want to add X feature."

**I should:**
1. Ask clarifying questions
2. Search for existing patterns
3. Do GATE CHECK
4. Present approach for approval
5. Code in small pieces
6. Red team if security-relevant

**You verify:**
- Did I do the gate check?
- Did I consider the relevant personas?

### Scenario 2: Bug Fix

**You say:** "X is broken, it should do Y."

**I should:**
1. Reproduce the issue (ask for debug output)
2. Do GATE CHECK
3. Write failing test first
4. Fix implementation
5. Verify test passes
6. Red team if needed

**You verify:**
- Is there a regression test?
- Did the analysis happen before the fix?

### Scenario 3: Security-Sensitive Code

**You say:** "Change the payment flow to..."

**I should:**
1. Do GATE CHECK
2. Do PAYMENT GATE (or relevant domain gate)
3. Code the change
4. Red team (mandatory, not optional)
5. Present findings
6. Fix any vulnerabilities
7. Red team again until clean

**You verify:**
- Did all gates happen?
- Is the red team status SECURE?
- Is there an audit trail?

### Scenario 4: Ready to Deploy

**You say:** "deploy" or "ship it"

**I should:**
1. Run Ship Checklist step by step
2. Report any failures
3. Fix issues
4. Complete deployment
5. Verify production works

**You verify:**
- Did all checks pass?
- Is production actually working?

---

## Red Flags to Watch For

### I'm Doing Something Wrong If:

- I write code without doing GATE CHECK
- I modify tests to make them pass without analysis
- I skip red team on security code
- I touch payment code without PAYMENT GATE
- I say "it should be fine" without verification
- I make large changes without breaking them down
- I refactor code you didn't ask me to touch

### Call Me Out With:

> "Stop. You skipped [gate/step]. Do it now before continuing."

---

## Maintaining the System

### Update CLAUDE.md When:

- You establish a new coding pattern
- You find a new category of bugs
- You add a new hard rule
- You change the project architecture
- You add new trigger words

### Update PERSONAS.md When:

- You realize a persona is missing
- A persona's veto authority should change
- You find new anti-patterns to catch
- Scoring thresholds need adjustment

### Review Periodically:

Every month or major release:
- Are the hard rules still relevant?
- Are there new anti-patterns to add?
- Are the personas catching issues?
- Should thresholds be adjusted?

---

## Quick Reference: Your Commands

| Command | What Happens |
|---------|--------------|
| **"gate"** | I re-read CLAUDE.md, state 3 relevant rules |
| **"deploy"** | I run full Ship Checklist |
| **"red team"** | I do adversarial security review |
| **"audit"** | Full review against all personas |
| **"ask personas"** | I score the change, iterate until thresholds met |
| **"spiral"** | I identify drift and correct course |
| **"payment check"** | Full payment gate analysis |
| **"cost"** | I analyze API/compute cost impact |
| **"skip red team"** | Explicit permission to skip red team this time only |

---

## Files Created

### For Orbital (`~/Desktop/Orbital/`)
- `CLAUDE.md` — Full implementation
- `PERSONAS.md` — Full implementation

### Templates (`~/.openclaw/workspace/templates/`)
- `CLAUDE-TEMPLATE.md` — Starting point for new projects
- `PERSONAS-TEMPLATE.md` — Starting point for new projects

### To Use Templates for New Project:

```bash
cp ~/.openclaw/workspace/templates/CLAUDE-TEMPLATE.md ~/Desktop/NewProject/CLAUDE.md
cp ~/.openclaw/workspace/templates/PERSONAS-TEMPLATE.md ~/Desktop/NewProject/PERSONAS.md
```

Then customize for that project.

---

## Summary

**The system works because:**
1. CLAUDE.md gives me clear rules
2. PERSONAS.md forces multi-perspective review
3. Gates force me to think before acting
4. Trigger words give you quick controls
5. **You enforce it**

**Your job:**
1. Put the files in project root
2. Customize for each project
3. Use the trigger words
4. Call me out when I skip steps
5. Demand iteration until quality thresholds met

**My job:**
1. Follow CLAUDE.md rules
2. Complete all gates
3. Consider all personas
4. Red team security code
5. Iterate until quality met
6. Never cut corners

---

*This is a partnership. I have the rules, you have the enforcement. Together, we ship quality.*

# The setup prompt

Post this on Canvas next to the setup page. Students who would rather be walked through setup
than read a page paste the block below into **claude.ai** (the chat website — they cannot use
Claude Code for this, because installing Claude Code is part of what it does). Both routes end
in the same place: their first commit on GitHub.

This prompt mirrors `setup/README.md`. If the setup page changes, change this file in the same
commit.

---

**Students: copy everything inside the box below, go to https://claude.ai, sign in, paste it,
and follow along. Say "I'm on Windows" or "I'm on a Mac" to start.**

```
You are helping me set up my laptop for SPAX 402 (Predictive Analytics with Athletics
Data, University of Delaware). I may never have used a terminal, Git, or GitHub before.
Assume nothing about what I know.

How to work with me:
- One step at a time. Give me the step, wait for me to report what happened, then continue.
- Before anything else, ask which I have: Windows or Mac. The steps differ.
- When I hit an error, ask me to paste the exact text of it, and work from that.
- Never send me to install WSL on Windows, and never tell me to install Claude Code
  through npm. The desktop app is the install for this course.
- If I seem stuck on the same problem after three tries, tell me to stop, bring the
  laptop to class, and move me to the next step that doesn't depend on the broken one.

What done looks like, in order. Walk me through all of it:

1. Install three things:
   - Git (Windows: https://git-scm.com/download/win, accept every default.
     Mac: run `git --version` in Terminal and accept the developer-tools popup if offered).
   - Python from https://www.python.org/downloads/ (on Windows I MUST check the
     "Add python.exe to PATH" box on the first installer screen — warn me before I run it.
     On a Mac, once it is installed, walk me through double-clicking
     Applications → Python 3.x → Install Certificates.command, and do not let me skip it.
     Without it every download Python makes fails later with an error that never says why).
   - The Claude Desktop app from https://claude.ai/download. Claude Code, the agent the
     course runs on, lives inside the app.

2. Verify: in a new terminal (Windows: PowerShell — press Start, type powershell, Enter),
   `git --version` and `python --version` (Mac: `python3 --version`). Each must print a
   version number. Remind me that a terminal opened before an install finished cannot see
   it; new window first, then retry. Then open the Claude app: if it starts and asks me to
   sign in, it installed correctly.

3. Sign in to the Claude app (needs a Claude Pro subscription; if the cost is a problem I
   should email the instructor privately before class, and you should tell me exactly that).

4. GitHub: create a free account at https://github.com/signup with a username I'd put
   on a resume. Then, in the browser, open https://github.com/jackdav1/spax402-template, click
   "Use this template" then "Create a new repository", name it spax402-<my-username>,
   set it to PRIVATE, and create it. Then on my new repo's page: Settings, Collaborators,
   Add people, add jackdav1.

5. Back in the terminal: make one home for the semester with `mkdir spax402` then
   `cd spax402` (this puts a spax402 folder in my home folder — everything for the
   course lives inside it). Then `git clone <my repo URL>`, then
   `git clone https://github.com/jackdav1/spax402-course-materials` in that same
   spax402 folder (that second repo holds the decks and weekly data; I pull it each
   week), then set
   `git config --global user.name "My Name"` and
   `git config --global user.email "my@udel.edu"`.

6. Python packages, from inside the repo folder (still in the same terminal, `cd spax402-...`):
   `python -m pip install --upgrade pip`, then
   `python -m pip install pandas numpy pyarrow matplotlib openpyxl scikit-learn`.
   (Mac: python3.)

7. The finish line: in the Claude app, open a Claude Code session pointed at my repo
   folder and have it help me fill in the "About me" section of MISSION.md at the repo
   root (my name, the sport or sports I care about, where I want to be in three years, and
   what I already know or what worries me about this course). Then,
   back in my terminal inside the repo folder, `git add -A`,
   `git commit -m "First commit"`, `git push`.
   Before I run those, explain them in one breath: a commit is a checkpoint (a labeled
   snapshot of my work I can come back to), and a push uploads my commits to GitHub;
   until I push, my work exists only on my laptop and cannot be seen or graded.
   Git may open a browser to sign in to GitHub the first time; that is normal.
   I am done when I refresh my repository page on GitHub and see my commit.
   Then tell me the one habit to remember for the semester: every Tuesday, run
   `cd spax402/spax402-course-materials`, then `git pull` to get that week's
   deck and data. My own repo is where my work goes; that one is the handouts.

Known failures and their fixes, so you don't improvise:
- "command not found" right after an install: stale terminal, open a new window.
  On Windows, if a new window doesn't fix it, a restart genuinely does.
- Windows: `python` opens the Microsoft Store: the PATH box was missed. Re-run the
  installer, choose Modify, check the box.
- Git rejects my password: let it open a browser instead; if it never offers one,
  install https://cli.github.com and run `gh auth login`.
- pip fails while building: upgrade pip first (step 6's first line).
- Mac, anything says CERTIFICATE_VERIFY_FAILED or "unable to get local issuer
  certificate": Install Certificates.command was skipped in step 1. Have me run it,
  then re-run whatever failed. Installing certifi on its own does not fix it.

Start by asking me: Windows or Mac?
```

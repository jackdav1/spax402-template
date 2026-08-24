# Setup — SPAX 402

Predictive Analytics with Athletics Data · University of Delaware · Fall 2026

Everything you install here, you install once. After Tuesday you will not think about any of it
again for the rest of the semester.

**Budget 30 to 45 minutes if you have never used a terminal.** Twenty if you have. Do it before
class if you can. If something breaks, skip to [Troubleshooting](#troubleshooting)
rather than guessing; every failure listed there has a two-line fix.

**Prefer being walked through it?** Canvas also has a setup prompt you can paste into
**https://claude.ai** in your browser, and Claude will take you through these same steps one at a
time, reading your error messages as you go. Same destination either way.

You need three things, and each one exists for a reason:

| What | Why this course needs it |
|---|---|
| **Git** | How your work gets from your laptop to GitHub, which is how it gets graded. On Windows it also supplies the shell Claude Code runs commands in. |
| **Python 3.11 or newer** | The analysis language. Claude Code writes the Python; you read the output. |
| **Claude Desktop app** | The agent. Claude Code runs inside it. A subscription is required, covered at the end. |

---

## Windows

Three installers.

### 1. Git for Windows

Download from **https://git-scm.com/download/win** and run it. The installer asks a lot of
questions; **accept every default**. The defaults are correct for this course, and one of them
installs Git Bash, which is the shell Claude Code uses on Windows.

### 2. Python

Download from **https://www.python.org/downloads/** and run it. There is exactly one box you must
not miss:

> ☑ **Add python.exe to PATH**

It is at the bottom of the first installer screen and it is unchecked by default. Check it before
you click Install. If you miss it, Windows will not be able to find Python and the error you get
back will not mention PATH at all. Re-running the installer and choosing Modify fixes it.

### 3. The Claude Desktop app

Download it from **https://claude.ai/download** and run the installer. Claude Code, the agent
this course runs on, lives inside the app.

Now skip ahead to [Verify the installation](#verify-the-installation).

**You do not need WSL.** If you have read elsewhere that Claude Code on Windows requires the
Windows Subsystem for Linux, that is out of date. It runs natively, and installing WSL will cost
you an hour and give you a second machine to keep track of.

---

## macOS

Open **Terminal** (press Command-Space, type `terminal`, press Enter).

### 1. Git

You may already have it. Type this and press Enter:

```
git --version
```

If it prints a version number, you are done with this step. If macOS pops up a dialog offering to
install developer tools, accept it and wait; that installs Git.

### 2. Python

macOS ships an old Python that will fight you. Install a current one from
**https://www.python.org/downloads/** and accept the defaults. It installs alongside the system
one rather than replacing it, which is what you want.

### 3. The Claude Desktop app

Download it from **https://claude.ai/download**, open the file, and drag Claude into
Applications. Claude Code, the agent this course runs on, lives inside the app.

---

## Verify the installation

Open a **new** terminal window (on Windows: press the Start key, type `powershell`, press Enter;
on macOS: Terminal) and run these two lines, one at a time. New window matters: a shell that was
already open does not know about anything you installed since.

```
git --version
```
```
python --version
```

You are looking for a version number from each. Rough floors: Git 2.40 or newer, Python 3.11 or
newer. Newer than that is fine.

Then open the Claude app. If it starts and asks you to sign in, it installed correctly.

On macOS, `python --version` may fail while `python3 --version` works. That is normal and nothing
in this course breaks because of it. Use `python3` wherever these instructions say `python`.

If either command says something like `command not found` or `is not recognized`, that one did
not install, or your shell has not noticed it yet. Close the window, open a new one, and try
again before assuming it failed.

---

## Sign in to Claude

Claude needs a **Claude Pro** subscription, about $20 a month.

Once you have an account, open the Claude app and sign in. That's the whole step: the app
remembers you from then on.

---

## Get your repo

You create your own private course repository from the course template. You need a free GitHub
account first: **https://github.com/signup**.

Use whatever username you like. The instructor sees it every week, so pick something you would
put on a resume.

Then, in a browser:

1. Open the course template: **https://github.com/jackdav1/spax402-template**.
2. Click the green **Use this template** button, then **Create a new repository**.

   ![The green "Use this template" button, top right of the repository page](use-this-template.png)

3. Name it `spax402-<your-username>` and set it to **Private**. Create it.
4. On your new repo's page: **Settings → Collaborators → Add people**, and add **`jackdav1`**.
   This is how your work gets graded; without it the instructor cannot see your repo.
5. Paste your repo's URL into the Week 1 Canvas assignment.

Then copy the same URL and, in your terminal:

```
git clone <paste-the-url-here>
```

The first time you push work, Git will ask who you are. Answer once:

```
git config --global user.name "Your Name"
```
```
git config --global user.email "you@udel.edu"
```

Git may also ask you to sign in to GitHub when you first push. Do it in the browser window it
opens. It only asks once per machine.

---

## Install the Python packages

Move into your repo (`cd spax402-your-name`, using whatever your folder is actually called), then:

```
python -m pip install --upgrade pip
```
```
python -m pip install pandas numpy pyarrow matplotlib openpyxl scikit-learn
```

That is the whole toolkit for the semester. Without `pyarrow` the NFL data will not open.

On macOS, use `python3` instead of `python` in both lines.

---

## First commit

You are set up when a commit of yours is on GitHub. In the Claude app, open a **Claude Code**
session and point it at your repo folder (the `spax402-...` folder you just cloned).

Your repo has a `MISSION.md` at its root: what you want out of this course, in your own words.
Ask Claude Code to help you fill in the **About me** section — your name, the sport you care
about, where you want to be in three years. That edit is your first commit. Then back in your
terminal, inside the repo folder:

```
git add -A
```
```
git commit -m "First commit"
```
```
git push
```

Refresh your repository page on GitHub. If your commit is there, the tooling half of this course
is behind you for the semester.

---

## Troubleshooting

**`git` or `python` is not recognized, right after installing it.**
Your terminal was open before the install finished. Close the window, open a new one, try again.
If a new window does not fix it on Windows, restart the machine. This is the one problem a
restart genuinely solves.

**On Windows: `python` opens the Microsoft Store.**
You missed the "Add python.exe to PATH" checkbox. Re-run the Python installer, choose Modify, and
check it.

**Git asks for a password and rejects the one you type.**
GitHub stopped accepting account passwords over the command line. When it prompts, let it open a
browser and sign in there instead. If it never offers a browser, install the GitHub CLI from
**https://cli.github.com** and run `gh auth login`.

**`pip install` fails while building something.**
Almost always an old pip. Run the `python -m pip install --upgrade pip` line first; it is easy to
skip.

**Anything else.** Bring the laptop to class Tuesday, or email the instructor with the exact text
of the error. "It didn't work" cannot be debugged; the last ten lines of red text usually can be,
in about a minute.

---

## FAQs

**Do I need to set up an MCP server so Claude Code can use GitHub?**
No. Claude Code runs `git` and, if you install it, the `gh` command directly in your terminal,
which is all this course needs. A GitHub MCP server is an optional extra that adds a token to
manage and buys you nothing here. MCP comes up in Week 12.

**Do I need to know Python?**
No. You need to read output and judge whether it is right, which is what the course teaches. You
will end up recognising a fair amount of Python by December without setting out to.

**Can I use a different agent, or a different editor?**
The course is built on Claude Code and every weekly command depends on it. Use whatever editor you
like for reading files.

**Is any of my work private?**
Your repository is private to you and the instructor. Everything in it, including your Claude
transcripts, is read as part of grading. Nothing you put there is private from the instructor:
the transcript is a large part of what gets graded.

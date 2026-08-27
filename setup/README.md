# Setup — SPAX 402

Predictive Analytics with Athletics Data · University of Delaware · Fall 2026

Everything you install here, you install once. After Tuesday you will not think about any of it
again for the rest of the semester.

We do this together in class on Tuesday. If something breaks, skip to
[Troubleshooting](#troubleshooting) rather than guessing; every failure listed there has a
two-line fix.

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

**Then do one more step that the installer does not do for you.** Open **Finder → Applications →
Python 3.x** and double-click **Install Certificates.command**. A terminal window opens, prints
a few lines, and closes.

That step gives Python the list of certificate authorities it uses to confirm a download really
came from where it claims. Without it, anything Python downloads over the internet fails, and the
error it prints (`CERTIFICATE_VERIFY_FAILED`) never mentions certificates being missing. Safari
and Git are unaffected, so the machine looks fine right up until Python tries. Thirty seconds now
saves an hour in week three.

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

Now pick where both course folders will live on your computer. One folder holds everything for
the semester. Open a terminal and make it:

```
mkdir spax402
```
```
cd spax402
```

That creates a folder named `spax402` in your home folder (`C:\Users\yourname\spax402` on
Windows, `/Users/yourname/spax402` on a Mac) and moves you into it. Every command below runs
from inside it. If you close the terminal and open a fresh one later, get back to your repo with
a single `cd spax402/spax402-your-name`.

Copy your repo's URL and clone it:

```
git clone <paste-the-url-here>
```

Then clone the course materials repo next to it — decks and weekly data live there, and each
week you will `git pull` inside it to get the new content:

```
git clone https://github.com/jackdav1/spax402-course-materials
```

When you are done, the `spax402` folder contains exactly two folders: `spax402-yourname` (your
work, gets pushed) and `spax402-course-materials` (the handouts, gets pulled).

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

Still in the same terminal, move into your repo (`cd spax402-your-name`, using whatever your
folder is actually called), then:

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

Two words you will use every week. A **commit** is a checkpoint: it snapshots your work with a
label, like saving your game, and you can always come back to it. A **push** uploads your commits
to GitHub. Until you push, your work exists only on your laptop and cannot be seen or graded.
The rhythm is always: save the file, commit the checkpoint, push it to GitHub.

You are set up when a commit of yours is on GitHub. In the Claude app, open a **Claude Code**
session and point it at your repo folder (the `spax402-...` folder you just cloned).

Your repo has a `MISSION.md` at its root: what you want out of this course, in your own words.
Ask Claude Code to help you fill in the **About me** section — your name, the sport or sports
you care about, where you want to be in three years, and what you already know or what worries
you about this course. That edit is your first commit. Then back in your terminal, inside the
repo folder:

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

## Getting each week's files

New decks and data are posted to the `spax402-course-materials` folder you cloned above. Your
own repo does not update itself; new course files only ever arrive in that second folder, and
you fetch them by opening a fresh terminal and running two lines at the start of each week:

```
cd spax402/spax402-course-materials
```
```
git pull
```

(If the terminal says `No such file or directory`, you are not where you think you are; a fresh
terminal always starts in your home folder, which is where `spax402` lives.)

When a weekly assignment points at a data file, look in your own repo's `weeks/` folder first;
if it is not there, it is in `spax402-course-materials` after a pull. Copy it into the matching
`weeks/` folder of your own repo before working on it, so your work and its inputs get pushed
together.

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

**On macOS: something says `CERTIFICATE_VERIFY_FAILED` or `unable to get local issuer
certificate`.**
You skipped **Install Certificates.command** in the Python step above, or you have an older
Python that was installed without it. Go run it now: **Applications → Python 3.x → Install
Certificates.command**. Nothing was downloaded and nothing was damaged, so re-run whatever
failed afterwards. Installing the `certifi` package instead does not fix this on its own.

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
Your repository is private to you and the instructor. Everything in it, including your quiz and
audit transcripts, is read as part of grading. Nothing you put there is private from the
instructor: those transcripts are a large part of what gets graded. Your free-form Claude Code
conversations stay on your laptop and are not part of the repo.

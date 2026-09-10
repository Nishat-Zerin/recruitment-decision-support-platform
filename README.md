# AI-Assisted Recruitment Decision Support Platform

## What is this?

A tool I built to help a recruiter go through hundreds of job applications faster — without unfairly rejecting good people, and without ever letting the AI make the final call.

## Why I built this

Picture this: a company posts one job opening and gets 500 CVs. Someone has to actually read every single one to figure out who's qualified. That takes days, it's exhausting, and two different recruiters reading the same CV will often judge it differently.

A lot of companies have tried to fix this with automated tools, but those tools quietly created a new problem. They often reject genuinely good candidates just because their CV has an unusual layout — a two-column design, a creative template, anything a bit non-standard — even if the person is perfectly qualified. That's not really about skill anymore, it's about formatting luck.

There's a second, sneakier bias too. Recruiters going through applications as they arrive tend to be more generous with the first few people they read, and more tired and critical by CV number 300 — even if that 300th person is actually the stronger candidate. So *when* you happened to apply can end up mattering more than it should.

I wanted to build something that fixes both of these without just replacing one black box with another.

## What I was actually going for

- **Faster** — a recruiter works from a ranked list instead of reading every CV cold
- **Fairer** — nobody gets quietly rejected for how their CV looks, and applying early or late doesn't change your odds
- **Explainable** — every recommendation comes with an actual reason, not just a mystery percentage
- **Human-controlled** — the AI only ever suggests. A person decides. Always.

## What makes this different from other AI screening tools I've seen

Most "AI hiring" tools work like this: upload CVs, get a score, low scores get auto-rejected, and nobody really knows why. That's fast, but it's a black box, and it can be unfair without anyone ever noticing.

I did two things differently here:

1. **If a CV can't be read cleanly** — bad formatting, a scanned image, an unusual template — it does *not* get scored low and quietly dropped. It gets flagged as "needs a human look," kept clearly separate from candidates who are genuinely a weaker match. Nobody just disappears from the list.
2. **Every recommendation comes with a real explanation.** Not "72% match" and nothing else — you can click a button and see the actual reasoning: which skills matched, what's missing, and why that candidate ended up where they did.

## Why this actually matters

For a company using this in practice: faster shortlisting, fewer strong candidates lost to formatting quirks, and a hiring process you could actually explain if someone asked "why was this person ranked here?" — which matters more than it used to, since regions like the EU now legally expect companies to be able to explain AI-driven hiring decisions, not just point at a score.

## What it looks like

**Uploading a job and a batch of CVs:**

![Upload screen](./upload-screen.png)

**The ranked list, with a real explanation pulled up for the top candidate:**

![Candidates screen](./candidates-screen.png)

## Want the full story?

- 📄 [Case Study](./AI-Recruitment-Platform-Case-Study.pdf) — the problem, the design decisions, how it stacks up against existing tools, and what I'd build next
- 📄 [Business Requirements Document](./AI-Recruitment-Platform-BRD.pdf) — the detailed technical requirements, written the way a real one would be at a company

## How it actually works, simply put

1. A recruiter uploads a job description and a batch of CVs
2. The system compares each CV against what the job needs
3. Candidates land in one of two lists — a main ranked list, or a "needs a human look" list if something couldn't be read reliably
4. Clicking a candidate shows a plain-English explanation of their ranking — written by an AI model, but only using facts actually found in their CV, never invented
5. A separate tracker page shows people moving through stages: Shortlisted → Interview → Hired

## Want to run it yourself?

```bash
pip install -r requirements.txt
```

Grab your own free [Groq](https://console.groq.com) API key, paste it into `app.py` (replacing `PASTE_YOUR_GROQ_API_KEY_HERE`), then:

```bash
streamlit run app.py
```.

## Built with

Python, Streamlit, and Groq's API (running an open-weight AI model)

# CrewAI Multi-Agent Reel Generator

This project uses **CrewAI** to create Instagram reel content using 3 AI agents.

## Architecture

```text
User Theme
    ↓
Content Ideator
    ↓
Reel Concept
    ↓
Script Writer
    ↓
Reel Script
    ↓
Engagement Optimizer
    ↓
Final Reel Package
```

## Agents

### 1. Content Ideator

Responsible for generating reel ideas.

```python
content_ideator = Agent(...)
```

Its job is to:

* Generate multiple reel concepts
* Choose the best concept
* Suggest audio and visual style

### 2. Script Writer

Converts the selected concept into a complete script.

```python
script_writer = Agent(...)
```

Its job is to:

* Create a strong hook
* Write the dialogue
* Define shots and timing
* Add text overlays

### 3. Engagement Optimizer

Improves the final reel for engagement.

```python
engagement_optimizer = Agent(...)
```

Its job is to:

* Improve the hook
* Improve pacing
* Create the caption
* Add hashtags
* Suggest posting time
* Add a CTA

---

## Tasks

A **Task** is the specific piece of work assigned to an agent.

```python
task_ideate = Task(
    description="Generate 3 reel concepts...",
    agent=content_ideator
)
```

The important part is:

```python
agent=content_ideator
```

This explicitly connects the task to the agent.

Tasks are **not connected to agents by index**.

For example:

```text
content_ideator       → task_ideate
script_writer         → task_write_script
engagement_optimizer  → task_optimize
```

---

## Crew

```python
reel_crew = Crew(
    agents=[
        content_ideator,
        script_writer,
        engagement_optimizer
    ],

    tasks=[
        task_ideate,
        task_write_script,
        task_optimize
    ],

    process=Process.sequential
)
```

### `agents`

This tells CrewAI:

> These agents are part of this crew.

### `tasks`

This tells CrewAI:

> These are the tasks that need to be executed.

### `Process.sequential`

This tells CrewAI:

> Execute the tasks one after another.

Therefore:

```text
task_ideate
     ↓
task_write_script
     ↓
task_optimize
```

The **task list controls execution order**, while `agent=...` controls which agent performs each task.

---

## Context

The second task has:

```python
context=[task_ideate]
```

This means:

> Give the output of the ideation task to the script-writing task.

Similarly:

```python
context=[task_ideate, task_write_script]
```

means the optimizer receives the outputs of both previous tasks.

So the information flows like:

```text
Task 1
  ↓
Output 1
  ↓
Task 2
  ↓
Output 2
  ↓
Task 3
  ↓
Final Output
```

---

## Starting the Crew

```python
result = reel_crew.kickoff(
    inputs={
        "reel_theme": "A day in the life of a CSE student during placement season"
    }
)
```

`kickoff()` starts the workflow.

The `{reel_theme}` placeholder in Task 1 is replaced with the value supplied in `inputs`.

---

## Important Concepts

```text
Agent
= Who performs the work

Task
= What work needs to be done

Crew
= Collection of agents and tasks

Process.sequential
= Execute tasks in order

Context
= Pass previous task output to another task

kickoff()
= Start the workflow
```

The underlying LLM can be the same Gemini model for all three agents. Different `role`, `goal`, `backstory`, and `Task` instructions make the model behave differently for each job.

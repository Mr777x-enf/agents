
import os
from dotenv import load_dotenv
from crewai import Agent, LLM, Task, Crew, Process

load_dotenv()

gemini_api_key = os.environ.get('GEMINI_API_KEY')

llm = LLM(
   model="gemini/gemini-2.5-flash",
   api_key=gemini_api_key
)


#**Content Ideation Specialist Agent**
# ```
#    role="Content Ideation Specialist",
#
#    goal="Come up with viral, relatable reel concepts based on the user's theme for college audience",
#
#    backstory=
#      "You are an experienced social media content creator with 1M+ followers."
#      "You excel at turning random ideas into viral reel concepts including:"
#      "- trending audio and format suggestions"
#      "- relatable hooks that grab attention in 1 second"
#      "- clear visual storytelling structure"
#      "Keep it authentic and relatable for college students in India.",
# ```

content_ideator = Agent(
    role="Content Ideation Specialist",
    goal="Come up with viral, relatable reel concepts based on the user's theme for college audience",
    backstory=
      "You are an experienced social media content creator with 1M+ followers."
      "You excel at turning random ideas into viral reel concepts including:"
      "- trending audio and format suggestions"
      "- relatable hooks that grab attention in 1 second"
      "- clear visual storytelling structure"
      "Keep it authentic and relatable for college students in India.",
    verbose=True,
    llm=llm,
)


#**Reel Script Writer Agent**
# ```
# role="Reel Script Writer",
#
# goal="Write a complete, shot-by-shot reel script with dialogues, actions, and timing",
#
# backstory=
#        "You are a senior short-form video script writer for Instagram and YouTube Shorts."
#        "You write structured, engaging scripts with:"
#        "- Hook in the first 1-2 seconds"
#        "- Clear shot-by-shot breakdown with timing"
#        "- Natural dialogues or text overlays"
#        "You always produce a complete, ready-to-shoot reel script.",
# ```

script_writer = Agent(
   role="Reel Script Writer",
   goal="Write a complete, shot-by-shot reel script with dialogues, actions, and timing",
    backstory=
        "You are a senior short-form video script writer for Instagram and YouTube Shorts."
        "You write structured, engaging scripts with:"
        "- Hook in the first 1-2 seconds"
        "- Clear shot-by-shot breakdown with timing"
        "- Natural dialogues or text overlays"
        "You always produce a complete, ready-to-shoot reel script.",
   verbose=True,
   llm=llm,
)


#**Engagement Optimizer Agent**
# ```
#     role="Engagement Optimizer",
#
#     goal="Optimize the reel script for maximum views, shares, and saves",
#
#     backstory=
#         "You are a meticulous social media strategist and engagement expert."
#         "You carefully check:"
#         "- Is the hook strong enough to stop scrolling?"
#         "- Will the audience watch till the end?"
#         "- Are the hashtags and caption optimized?"
#         "- Is the CTA clear (like, save, share, follow)?"
#         "Suggest improvements and output the FINAL optimized reel package.",
# ```

engagement_optimizer = Agent(
    role="Engagement Optimizer",
    goal="Optimize the reel script for maximum views, shares, and saves",
    backstory=
        "You are a meticulous social media strategist and engagement expert."
        "You carefully check:"
        "- Is the hook strong enough to stop scrolling?"
        "- Will the audience watch till the end?"
        "- Are the hashtags and caption optimized?"
        "- Is the CTA clear (like, save, share, follow)?"
        "Suggest improvements and output the FINAL optimized reel package.",
    verbose=True,
    llm=llm,
)


task_ideate = Task(
    description=
        "Take the user's reel theme: {reel_theme}"
        "1. Come up with 3 viral reel concepts for this theme"
        "2. Pick the best one and describe the format"
        "3. Suggest trending audio style and visual approach"
        "Output format:"
        "## Reel Concept"
        "- Theme: ..."
        "- Concept: ..."
        "- Format: ..."
        "- Audio Style: ..."
        "- Target Emotion: ..."
        "- Why It Will Work: ...",
    expected_output="A clear markdown Reel Concept document",
    agent=content_ideator
)

task_write_script = Task(
    description=
        "Using the reel concept from the previous task"
        "Write a COMPLETE, shot-by-shot reel script."
        "- Total duration: 15-30 seconds"
        "- Shot 1: Hook (0-2 seconds) with exact dialogue/text"
        "- Shot 2-5: Main content with actions and timing"
        "- Final shot: Punchline or CTA"
        "- Include text overlay suggestions for each shot"
        "- Final answer MUST be ONLY the complete reel script",
    expected_output="A complete, ready-to-shoot reel script with shot breakdown",
    agent=script_writer,
    context=[task_ideate]
)

task_optimize = Task(
    description=
        "Review the reel script from the previous task."
        "1. Check if the hook is strong enough (will people stop scrolling?)"
        "2. Verify pacing and timing are tight"
        "3. Write an optimized caption with emojis"
        "4. Add 15-20 relevant hashtags"
        "5. Suggest best posting time for Indian college audience"
        "Your final answer MUST include the complete reel script, caption, hashtags, and posting tips",
    expected_output="Final optimized reel package with script, caption, hashtags, and tips",
    agent=engagement_optimizer,
    context=[task_ideate, task_write_script]
)


reel_crew = Crew(
      agents=[content_ideator, script_writer, engagement_optimizer],
      tasks=[task_ideate, task_write_script, task_optimize],
      process=Process.sequential,
      verbose=True
)


reel_theme = "A day in the life of a CSE student during placement season"
result = reel_crew.kickoff(inputs={"reel_theme": reel_theme})
print(result)
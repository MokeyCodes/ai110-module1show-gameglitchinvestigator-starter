# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- The game kept saying "HIGHER" when the score was 5.
- Updating the list required the user to enter a new number first.
- The New Game button doesn't work
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude (claude.ai) and GitHub Copilot on this project. Claude was my main collaborator — I shared the code files and asked it to help identify bugs, refactor logic into logic_utils.py, and write tests. Copilot helped with smaller autocomplete suggestions while editing files in my editor.
One example where Claude was correct: it identified that the check_guess function had a broken string-comparison fallback that would kick in on a TypeError, potentially returning wrong outcomes. I verified this by writing a test (test_guess_too_high) and confirming it passed only after the fallback was removed.
One example where I had to think critically: Claude's initial update_score fix removed the +5 reward for "Too High" on even attempts and replaced it with a flat -5 for all wrong guesses. This made the scoring more consistent, but it also meant winning late in the game could result in a negative final score — as I saw when I won with a score of -10. The logic was technically correct per the fix, but it showed that AI suggestions still need to be evaluated against the actual user experience.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when both a manual test in the browser and a pytest test confirmed the correct behavior. For example, after fixing check_guess, I ran pytest test_logic_utils.py and watched test_guess_too_high and test_guess_too_low pass, then also verified in the running app that the hints pointed the right direction.
The most revealing test was test_win_late_gives_minimum_10, which confirmed the max() cap was working — without it, winning on a late attempt could theoretically return a negative score from the win bonus calculation alone. Claude helped me think of that edge case, which I wouldn't have tested on my own right away.
Claude also helped me understand why the tests in tests/test_game_logic.py were failing — they were written expecting a plain string return from check_guess, but the function returns a tuple. Adding the import and unpacking the tuple fixed all three failures immediately.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because Streamlit reruns the entire Python script from top to bottom every time a button is clicked or any input changes. Without protection, st.session_state.secret = random.randint(low, high) ran on every rerun, picking a new secret each time.
I would explain Streamlit reruns to a friend like this: imagine every time you click a button on a webpage, the entire page reloads and re-executes all its setup code. Streamlit's session_state is like a sticky notepad that survives those reloads — anything you save there stays put between reruns.
The fix was wrapping the secret assignment in if "secret" not in st.session_state, so it only picks a number once at the start of a new game and never again until the player resets.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is writing tests immediately after refactoring, not at the end. On this project, having pytest catch the NameError in tests/test_game_logic.py saved me from a confusing runtime bug later. Running tests right after each change made it much easier to know exactly what broke and when.
One thing I'd do differently next time is verify AI-suggested fixes against the full user experience, not just whether the tests pass. The scoring fix was technically correct but produced a negative final score, which I only discovered by actually playing the game. Tests alone don't always catch whether something feels right.
This project changed how I think about AI-generated code — it's a strong first draft, but it needs a human to play the game, read the output, and ask "does this actually make sense?" AI is great at spotting patterns and writing boilerplate, but judgment about whether behavior feels correct still has to come from me.

# The Coderbyte format


<p class="lede">What your iFood warm-up showed, and how not to lose the first five minutes.</p>
<pre class="code">def FirstFactorial(num):     # num arrives as TEXT: "4", not 4
    n = int(num)               # convert first
    ...
    return result

# keep this function call here
print(FirstFactorial(input()))</pre>
<ul>
<li><b>input() is always a string.</b> Convert: <code>int(s)</code>, <code>float(s)</code>, <code>s.split(",")</code>, <code>[int(x) for x in s.split()]</code>.</li>
<li><b>Return what's asked, in the format asked.</b> If they want the text <code>true</code>, return <code>"true"</code>, not <code>True</code>.</li>
<li><b>Run Code</b> uses the input box; <b>Run Test Cases</b> may include hidden cases. Try edge cases yourself first: empty, one item, ties, negatives.</li>
<li><b>Playback:</b> they can replay your session afterwards with tab switches and copy-pastes timestamped. Say "I'll check the docs" before switching tabs.</li>
<li><b>iFood's rules (from the recruiter):</b> Coderbyte's built-in AI is off, but you may use another assistant (Claude, ChatGPT) in another window. You must explain the code afterwards, and <b>the interviewer evaluates the prompts you write</b>. Documentation is provided inside the exercise. Python is fine. Because tab switches are recorded, say "switching to my assistant" each time.</li>
<li><b>Focus:</b> software engineering for ML systems in production: robust, deterministic, reliable code that copes with real data and common model failures. Practise the "Robust ML systems" drills and lesson 1b.</li>
<li><b>Python 3.11</b> with numpy, pandas, scikit-learn, torch, transformers, sentence-transformers, langchain and mlflow installed, so you can import them if the task allows.</li>
<li>The invite says they'll talk about <b>your decisions and approach</b> while you code. The routine in lesson 0 is how you do that.</li>
</ul>
<p>Practise: the "Coderbyte-style" drills use exactly this shape, with an input box like the real editor.</p>

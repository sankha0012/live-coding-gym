const main = document.getElementById("main");
let DEV = false; // dev mode: everything open and revealed, no progress shown
let tick = null; // the running timer, cleared on every route change

async function api(path, body) {
  const opts = body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  };
  const r = await fetch("/api" + path, opts);
  if (!r.ok) throw new Error((await r.json()).detail || r.statusText);
  return r.json();
}

// h("div", {class: "row", onclick: fn}, child, "text", ...) builds a DOM node.
// Text is always inserted as text, never as HTML, except the explicit `html` attribute.
function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "html") el.innerHTML = v;
    else el.setAttribute(k, v);
  }
  for (const kid of kids.flat()) if (kid !== null && kid !== undefined) el.append(kid);
  return el;
}

const md = (text) => h("div", { html: marked.parse(text) });
const fmt = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

function editor(parent, kind, value) {
  return CodeMirror(parent, {
    value, mode: kind === "sql" ? "text/x-sql" : "python", lineNumbers: true, indentUnit: 4,
    extraKeys: { Tab: (cm) => cm.replaceSelection("    ") },
  });
}

// Starts a visible clock and returns a function giving elapsed seconds.
function startTimer(el, limit) {
  const t0 = Date.now();
  const elapsed = () => (Date.now() - t0) / 1000;
  clearInterval(tick);
  tick = setInterval(() => {
    const s = elapsed();
    el.textContent = limit ? `${fmt(s)} / ${fmt(limit)}` : fmt(s);
    el.className = "timer" + (limit && s > limit ? " bad" : "");
  }, 500);
  return elapsed;
}

// tip(el, text): hover tooltip (also read by screen readers).
function tip(el, text) { el.setAttribute("data-tip", text); el.setAttribute("title", text); el.classList.add("tip"); return el; }

const COMPETENCY = {
  C1: "Work comfortably on Coderbyte: stdin, stdout, run, test", C2: "Production-quality Python for ML systems",
  C3: "Robust code: validate input, handle failure", C4: "Deterministic code: same input, same output",
  C5: "Reliable code: retries, timeouts, fallbacks, idempotency", C6: "Real data behaviour: nulls, duplicates, joins, time",
  C7: "Common model failures in production", C8: "Steer the assistant with good prompts", C9: "Explain every line afterwards",
  C10: "Find answers in the documentation you are given",
};
const GROUP_INFO = {
  Read: "Understand code before you touch it: what happens if one line changes?",
  Build: "Plan, ask the assistant for small pieces, run, then prove control.",
  Catch: "Find what the assistant got wrong.",
  Defend: "Answer the follow-up questions an interviewer asks.",
};
const KIND_INFO = {
  python: ["Python", "Write a function in Python. Hidden tests check it, like Coderbyte."],
  sql: ["SQL", "Write a SQL query. Its result is compared with a reference result."],
  tests: ["Write tests", "Write pytest tests. They must pass on the correct code and fail on every buggy version."],
  quiz: ["Quiz", "Multiple choice, graded instantly. Wrong answers come with an explanation."],
  open: ["Open question", "Answer in your own words. An AI interviewer scores it against a rubric."],
  prompt: ["Prompt", "Write the prompt you would give an AI assistant. An AI interviewer scores the prompt."],
  explain: ["Explain code", "Explain the code as you would to the interviewer. An AI interviewer scores it."],
  read: ["Read code", "Read a script and say what happens when one line changes. No writing code."],
  triage: ["Accept or reject", "The assistant proposed changes. Decide which to accept and say why."],
};

function kindBadge(kind) {
  const [label, info] = KIND_INFO[kind] || [kind, ""];
  return tip(h("span", { class: "badge" }, label), info);
}

function mark(value) {
  if (value === null) return null;
  return h("span", { class: value ? "ok" : "bad" }, value ? "✓" : "✗");
}

const CHIP_INFO = {
  tests: "Hidden tests: passed once. For readings: the What if round answered right.",
  review: "AI review: every criterion at or above the step's minimum score.",
  explain: "The assistant wrote code for this exercise, so you show you understand it with a What if round.",
  fix: "Change the code so that it prints the target output.",
  control: "Control check: explain two lines of your own code, then make one small change by hand with the assistant locked.",
  bug: "Name the bug in one sentence after you fixed it. An AI interviewer compares it with the real cause.",
  prompts: "The prompts you typed to the assistant must pass the AI prompt review (small, clear, with constraints).",
  assisted: "You asked the assistant to write code for this exercise.",
};

function statusLine(st, kind) {
  if (DEV) return h("span");
  const chip = (key, label) => (st[key] === null ? null
    : tip(h("span", { class: "chip " + (st[key] ? "done" : "todo") }, label, " ", mark(st[key])), CHIP_INFO[key]));
  return h("span", {}, chip("tests", kind === "read" ? "what if" : "tests"), chip("review", "AI review"),
    chip("explain", "what if"), chip("fix", "fix it"), chip("control", "control check"), chip("bug", "name the bug"), chip("prompts", "prompts"),
    st.assisted ? tip(h("span", { class: "chip assisted" }, "assisted"), CHIP_INFO.assisted) : null);
}

function reviewBox(rev, onRetry) {
  if (!rev) return null;
  const box = h("div", { class: "review" });
  if (rev.status === "pending") {
    box.append(h("p", { class: "bad" }, rev.feedback), h("button", { onclick: onRetry }, "Retry review"));
    return box;
  }
  box.append(h("p", {}, h("strong", {}, rev.verdict)));
  for (const [criterion, score] of Object.entries(rev.scores)) {
    box.append(h("div", {}, `${score}/5  ${criterion}`));
  }
  box.append(h("p", {}, rev.feedback));
  return box;
}

function extrasPanel(ex) {
  const wrap = h("div");
  if (ex.hint) wrap.append(h("details", {}, h("summary", {}, "Hint"), md(ex.hint)));
  if (ex.guide) wrap.append(h("details", { class: "reveal" }, h("summary", {}, "Walkthrough: how to think about it"), md(ex.guide)));
  if (ex.reference) {
    const kind = ex.kind === "sql" ? "sql" : "python";
    wrap.append(h("details", { class: "reveal" }, h("summary", {}, ex.kind === "tests" ? "Reference tests" : "Reference solution"),
      h("pre", {}, ex.reference), h("p", { class: "muted" }, kind === "sql" ? "Other correct queries exist." : "Other correct solutions exist. Yours does not have to match.")));
  }
  if (ex.bug) wrap.append(h("details", { class: "reveal" }, h("summary", {}, "The bug"), md(ex.bug)));
  if (ex.change_solution) wrap.append(h("details", { class: "reveal" }, h("summary", {}, "Reference solution of the control-check change"), h("pre", {}, ex.change_solution)));
  if (ex.say) wrap.append(h("details", {}, h("summary", {}, "How to say it out loud"), md(ex.say)));
  if (ex.model_prompt) wrap.append(h("details", {}, h("summary", {}, "A good prompt for an AI assistant"), md(ex.model_prompt)));
  return wrap;
}

function nextBar(ex, passed) {
  const bar = h("div", { class: "bar" });
  if (passed) bar.append(h("strong", { class: "ok" }, "✓ Passed."));
  bar.append(ex.next
    ? h("a", { class: passed ? "button" : "", href: `#/ex/${ex.next.id}` }, "Next: " + ex.next.title + " →")
    : h("a", { href: `#/step/${ex.step_id}` }, "Back to the step"));
  return bar;
}

function quizView(ex) {
  const picks = ex.quiz.map(() => null);
  const note = h("div");
  const boxes = ex.quiz.map((q, i) => h("div", { class: "review" },
    h("p", {}, h("strong", {}, `${i + 1}. ${q.q}`)),
    q.options.map((o, j) => h("label", { style: "display:block" },
      h("input", { type: "radio", name: `q${i}`, onchange: () => { picks[i] = j; } }), " " + o,
      DEV && q.answer === j ? h("strong", { class: "ok" }, "  ← answer") : null)),
    DEV && q.why ? h("p", { class: "muted" }, q.why) : null));
  main.append(...boxes, h("div", { class: "bar" },
    h("button", { class: "primary", onclick: async () => {
      if (picks.includes(null)) { note.replaceChildren(h("p", { class: "bad" }, "Answer every question.")); return; }
      const r = await api("/quiz", { exercise_id: ex.id, answers: picks });
      r.results.forEach((res, i) => boxes[i].append(h("p", { class: res.correct ? "ok" : "bad" },
        (res.correct ? "✓ " : `✗ right answer: ${ex.quiz[i].options[res.answer]}. `) + res.why)));
      note.replaceChildren(h("p", {}, `${r.correct}/${r.total}. ` +
        (r.passed ? "Passed." : "Not yet: read the explanations, then try again."),
        " ", h("button", { onclick: route }, "Try again")), nextBar(ex, r.passed));
    } }, "Submit answers")), note);
}

function results(out, r, how) {
  out.textContent = "";
  if (how === "run" && !r.tests.length) {
    out.append(r.passed ? "✓ Ran without errors.\n" : "✗ Your code raised an error:\n");
    if (r.passed && !r.output.trim()) {
      out.append("Nothing was printed. Use print(...) to see values here, or press Submit to run the hidden tests.");
      return;
    }
  }
  for (const t of r.tests) out.append(`${t.passed ? "PASS" : "FAIL"}  ${t.name}\n`);
  out.append((r.tests.length ? "\n" : "") + r.output);
}

// ---------------- knowledge base: Reference pages and the exercise help sidebar ----------------
const helpPane = document.getElementById("help");
const helpToggle = document.getElementById("help-toggle");
let kbIndex = null;
async function kbList() { return kbIndex || (kbIndex = await api("/kb")); }

function setHelpOpen(open) {
  document.body.classList.toggle("help-open", open);
  helpToggle.textContent = open ? "Hide help ›" : "‹ Help";
  try { localStorage.setItem("helpOpen", open ? "1" : "0"); } catch (e) { /* private mode: just do not remember */ }
}
helpToggle.addEventListener("click", () => setHelpOpen(!document.body.classList.contains("help-open")));

function hideHelp() {
  helpPane.hidden = true;
  helpToggle.hidden = true;
  document.body.classList.remove("help-open");
}

function kbMatches(list, query) {
  const q = query.trim().toLowerCase();
  return list.filter((t) => (t.title + " " + t.summary + " " + t.tags.join(" ")).toLowerCase().includes(q));
}

const POLICY_NOTE = {
  train: "This assistant types code for you, but only one small piece per ask. Plan first, ask for one function, read every line, run it. Big asks are sent back.",
  explain: "This assistant explains only. It never writes code here. Use it to understand what a line or a script does.",
  off: "The assistant is off on this exercise. Find and fix the problem yourself, like in the real interview when it fails you.",
  free: "Interview conditions: the assistant writes code when you ask. Keep asks small and read what it gives you.",
};
const QUICK = [
  ["Explain the task", "Explain this task in plain words and tell me what to think about first. Do not give the solution."],
  ["Why does my code fail?", "My code fails or gives a wrong result. Look at my code and the last output, point at the likely problem and explain why, but do not rewrite it for me."],
  ["Review my code", "Review my current code for correctness, edge cases and readability. List the problems; do not rewrite it."],
];

// The assistant chat. ctx = { getCode(), getOutput(), getLine(), onAssisted(), grade } gives it the learner's current state.
function assistantPanel(scope, ctx) {
  const list = h("div", { class: "chat-list" });
  const note = h("p", { class: "muted chat-note" });
  const quick = h("div", { class: "chat-quick" });
  const gradeSlot = h("div");
  const error = h("p", { class: "bad" });
  const input = h("textarea", { class: "chat-input", rows: "3",
    placeholder: "Ask for ONE small piece. Enter sends, Shift+Enter adds a line." });
  const gradeBtn = tip(h("button", { onclick: async () => {
    gradeBtn.disabled = true;
    try { const rev = await api("/chat/grade", { scope }); gradeSlot.replaceChildren(reviewBox(rev, null)); if (ctx.onGraded) ctx.onGraded(); }
    catch (e) { gradeSlot.replaceChildren(h("p", { class: "bad" }, e.message)); }
    gradeBtn.disabled = false;
  } }, "Grade my prompts"), "An AI interviewer scores the prompts you typed here: clarity, size of each ask, constraints, whether you stay in control.");
  const clearBtn = tip(h("button", { onclick: async () => {
    if (!confirm("Clear this chat? (It will not undo the 'assisted' mark on this exercise.)")) return;
    await api("/chat/clear", { scope }); await load();
  } }, "Clear chat"), "Delete this conversation.");
  let state = { messages: [], policy: "train", locked: false };

  function decorate(box) {  // a Copy button on every code block
    box.querySelectorAll("pre").forEach((pre) => {
      const b = h("button", { class: "copy", onclick: async () => {
        try { await navigator.clipboard.writeText(pre.innerText.replace(/\nCopy$/, "")); b.textContent = "Copied"; }
        catch (e) { b.textContent = "Select and copy"; }
        setTimeout(() => { b.textContent = "Copy"; }, 1500);
      } }, "Copy");
      pre.append(b);
    });
  }
  function draw() {
    const off = state.policy === "off", locked = state.locked;
    note.textContent = locked ? "Locked: the control check is open. Make the change by hand; the assistant is back when you finish it." : POLICY_NOTE[state.policy];
    list.replaceChildren(...(state.messages.length ? state.messages.map((m) => {
      const box = m.role === "user" ? h("div", { class: "msg user" }, m.content) : h("div", { class: "msg assistant" }, md(m.content));
      if (m.role !== "user") {
        decorate(box);
        if (m.size) box.prepend(tip(h("span", { class: "chip " + (m.size === "large" ? "todo" : "done") }, m.size === "large" ? "large ask" : "small ask"),
          "How big your request was. Small asks keep you in control."));
      }
      return box;
    }) : [h("p", { class: "muted" }, off ? "" : "Ask about a concept, or for one small piece of code. Or use a quick button below.")]));
    list.scrollTop = list.scrollHeight;
    const can = !off && !locked;
    const lineBtn = h("button", { onclick: () => {
      const l = ctx.getLine && ctx.getLine();
      if (!l) { error.textContent = "Click a line in the editor first."; return; }
      send(`Explain this line in plain words: ${l}`);
    } }, "Explain this line");
    quick.replaceChildren(...(can ? [lineBtn, ...QUICK.map(([label, text]) => h("button", { onclick: () => send(text) }, label))] : []));
    input.disabled = !can;
    gradeBtn.hidden = !(ctx.grade && state.messages.some((m) => m.role === "user"));
  }
  async function send(text) {
    text = (text ?? input.value).trim();
    if (!text) return;
    error.textContent = "";
    input.value = "";
    state.messages.push({ role: "user", content: text });
    state.messages.push({ role: "assistant", content: "Thinking..." });
    draw();
    try {
      const r = await api("/chat", { scope, message: text, code: ctx.getCode(), output: ctx.getOutput() });
      const wasAssisted = state.assisted;
      state = { ...state, messages: r.messages, assisted: r.assisted, policy: r.policy, locked: r.locked };
      if (r.assisted && !wasAssisted && ctx.onAssisted) ctx.onAssisted();
    } catch (e) {
      state.messages.splice(-2, 2);
      input.value = text;
      error.textContent = e.message;
    }
    draw();
  }
  input.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } });
  async function load() {
    try { state = await api(`/chat?scope=${encodeURIComponent(scope)}`); }
    catch (e) { error.textContent = e.message; }
    draw();
  }
  const el = h("div", { class: "chat" },
    h("div", { class: "bar" }, h("strong", {}, "Assistant"), clearBtn),
    note, list, error, quick, input,
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: () => send() }, "Send"), gradeBtn), gradeSlot);
  el.refresh = load;
  load();
  return el;
}

// Tabs inside the right-hand sidebar.
function sidebarTabs(panes) {
  let saved = "help";
  try { saved = localStorage.getItem("helpTab") || "help"; } catch (e) { /* default */ }
  if (!panes.some((p) => p.id === saved)) saved = panes[0].id;
  const buttons = panes.map((p) => h("button", { class: "tab", onclick: () => show(p.id) }, p.label));
  function show(id) {
    panes.forEach((p, i) => { p.el.hidden = p.id !== id; buttons[i].classList.toggle("active", p.id === id); });
    try { localStorage.setItem("helpTab", id); } catch (e) { /* not remembered */ }
  }
  helpPane.replaceChildren(h("div", { class: "tabs" }, ...(panes.length > 1 ? buttons : [])), ...panes.map((p) => p.el));
  show(saved);
  helpPane.hidden = false;
  helpToggle.hidden = false;
  let open = true;
  try { open = localStorage.getItem("helpOpen") !== "0"; } catch (e) { /* keep default */ }
  setHelpOpen(open);
}

// The sidebar for one exercise: its relevant topics, a search over everything, articles opened in place, and the assistant.
function helpSidebar(ex, ctx) {
  const body = h("div");
  const search = h("input", { type: "search", placeholder: "Search the reference (e.g. join, sorted, window)" });
  const showArticle = async (id) => {
    const t = await api(`/kb/${id}`);
    body.replaceChildren(h("p", {}, h("button", { onclick: showTopics }, "← Back to this exercise's help")),
      h("h2", {}, t.title), md(t.body));
    helpPane.scrollTop = 0;
  };
  const topicLink = (t) => h("div", { class: "kb-hit" }, h("a", { href: `#/kb/${t.id}` }, t.title),
    h("div", { class: "muted" }, t.summary));
  function showTopics() {
    search.value = "";
    body.replaceChildren(ex.kb.length
      ? h("p", { class: "muted" }, "Concepts this exercise uses. Open one for syntax and examples. They explain the tools, not the answer.")
      : h("p", { class: "muted" }, "No topics are linked to this exercise yet. Use the search box above."),
      ...ex.kb.map((t) => h("details", { class: "kb-card" }, h("summary", {}, h("strong", {}, t.title),
        h("div", { class: "muted" }, t.summary)), md(t.brief),
        h("p", {}, h("a", { href: `#/kb/${t.id}` }, "Learn more →")))));
  }
  search.addEventListener("input", async () => {
    if (!search.value.trim()) return showTopics();
    const hits = kbMatches(await kbList(), search.value);
    body.replaceChildren(h("p", { class: "muted" }, `${hits.length} topic(s)`), ...hits.slice(0, 30).map(topicLink));
  });
  // Links to other articles open inside the sidebar, so the editor is never lost.
  body.onclick = (e) => {
    const a = e.target.closest("a");
    const href = a && a.getAttribute("href");
    if (href && href.startsWith("#/kb/")) { e.preventDefault(); showArticle(href.slice(5)); }
    else if (a) a.target = "_blank";
  };
  showTopics();
  const panes = [{ id: "help", label: "Help", el: h("div", {}, search, body) }];
  if (ex.kind !== "quiz") { ctx.assistantEl = assistantPanel(ex.id, ctx); panes.push({ id: "assistant", label: "Assistant", el: ctx.assistantEl }); }
  sidebarTabs(panes);
}

async function kbView(id) {
  if (id) {
    const t = await api(`/kb/${id}`);
    main.append(h("p", {}, h("a", { href: "#/kb" }, "← Reference")), h("h1", {}, t.title),
      h("p", { class: "muted" }, t.summary), md(t.body));
    return;
  }
  const list = await kbList();
  const results = h("div");
  const draw = (items) => {
    const groups = {};
    for (const t of items) (groups[t.tags[0] || "other"] = groups[t.tags[0] || "other"] || []).push(t);
    results.replaceChildren(...Object.keys(groups).sort().flatMap((g) => [h("h2", {}, g),
      ...groups[g].map((t) => h("div", { class: "row" }, h("a", { class: "grow", href: `#/kb/${t.id}` }, t.title),
        h("span", { class: "muted" }, t.summary)))]));
  };
  const search = h("input", { type: "search", placeholder: "Search " + list.length + " topics" });
  search.addEventListener("input", () => draw(kbMatches(list, search.value)));
  main.append(h("h1", {}, "Reference"),
    h("p", { class: "muted" }, "Short articles on the syntax and ideas the exercises use. The same articles open in the Help sidebar next to every exercise."),
    search, results);
  draw(list);
}

function stepRow(s, j) {
  const pct = s.total ? Math.round(100 * s.done / s.total) : 0;
  const need = s.total ? Math.round(100 * s.needed / s.total) : 0;
  const bar = tip(h("div", { class: "progress" }, h("div", { class: "fill", style: `width:${pct}%` }),
    s.optional ? null : h("div", { class: "needed", style: `left:${need}%` })),
    s.total ? `${s.done} of ${s.total} done.` + (s.optional ? "" : ` The marker shows the ${s.needed} needed to pass.`) : "No exercises here.");
  const label = s.optional ? h("span", { class: "muted" }, `optional · ${s.done}/${s.total}`)
    : s.passed ? tip(h("span", { class: "ok" }, "passed ✓"), "You finished enough of this step.")
    : s.total ? h("span", { class: "muted" }, `${s.done}/${s.total} (need ${s.needed})`) : h("span", { class: "muted" }, "mock rounds");
  const name = `${s.order}. ${s.title}`;
  const title = s.unlocked ? h("a", { href: `#/step/${s.id}` }, name)
    : tip(h("span", {}, `🔒 ${name}`), "Opens when you finish the step above, or unlock it yourself.");
  const row = h("div", { class: "row" + (s.unlocked ? "" : " locked") }, h("span", { class: "grow" }, title), DEV ? h("span", { class: "muted" }, `${s.total} core`) : bar, DEV ? null : label);
  if (!s.unlocked) {
    row.append(tip(h("button", { onclick: async () => { await api("/unlock", { step_id: s.id }); route(); } }, "Unlock"),
      "Open this step now without finishing the previous one."));
  }
  return row;
}

async function journeyView() {
  const j = await api("/journey");
  main.append(h("h1", {}, DEV ? "All steps (dev mode)" : "Your track"),
    h("p", { class: "muted" }, "The goal is control, not memorised syntax: read every line, steer the assistant in small steps, catch its mistakes, and explain what you ship. Work from the top. Each step opens when you finish most of the previous one."));
  if (j.errors.length) main.append(h("pre", { class: "bad" }, "Broken content:\n" + j.errors.join("\n")));
  if (DEV) main.append(h("p", { class: "notice" }, "Dev mode: every step is open, answers and reference solutions are shown, and no progress is displayed. Switch it off in the top bar."));
  else main.append(j.next
    ? h("div", { class: "bar" }, tip(h("a", { class: "button", href: `#/ex/${j.next.exercise_id}` }, "Continue: " + j.next.title),
        "Jumps to the next unfinished exercise, in " + j.next.step_title))
    : h("p", {}, "Every step is done. Run a mock round to test yourself."));
  if (!DEV) main.append(h("p", {},
    tip(h("span", {}, j.readiness === null ? "Readiness: not yet measured" : `Readiness: ${j.readiness}/100`),
      "Average score of your last three mock rounds. It is an estimate, not a promise."),
    "   ", h("a", { href: "#/cards" }, `Flashcards due today: ${j.due_cards}`)));
  for (const s of j.steps) main.append(stepRow(s, j));
  if (DEV) return;
  if (j.mocks.length) {
    main.append(h("h2", {}, "Mock round history"));
    for (const m of j.mocks) main.append(h("div", { class: "row" }, `${m.started_at}  score ${m.total}/100`));
  }
  main.append(h("h2", {}, "Reset"), h("div", { class: "bar" },
    tip(h("button", { class: "danger", onclick: async () => {
      if (!confirm("Delete ALL your progress: attempts, reviews, flashcard schedule, unlocked steps and mock scores? This cannot be undone.")) return;
      await api("/progress/reset", {});
      route();
    } }, "Reset all progress"), "Start again from zero. Your typed code drafts stay in this browser."),
    h("span", { class: "muted" }, "Deletes attempts, reviews, flashcards schedule, unlocks and mock scores.")));
}

async function stepView(id) {
  const s = await api(`/step/${id}`);
  const g = s.gate;
  main.append(h("p", {}, h("a", { href: "#/" }, "← Track")), h("h1", {}, s.title));
  if (s.intro) main.append(h("p", {}, s.intro));
  if (g.total && !s.optional && !DEV) {
    main.append(h("p", { class: "muted" },
      `Pass this step by finishing ${g.needed} of its ${g.total} required exercises (${g.done} done). ` +
      "Hover a badge or tick for what it means."));
  }
  if (s.lessons.length) main.append(h("h2", {}, "Read first"));
  for (const lesson of s.lessons) {
    main.append(h("details", {}, h("summary", {}, lesson.title), md(lesson.body)));
  }
  if (!s.exercises.length) {
    main.append(h("p", {}, "This step is practised with ", h("a", { href: "#/mock" }, "mock rounds"), "; your last three scores give the readiness estimate."));
    return;
  }
  const row = (ex) => h("div", { class: "row" },
    h("a", { class: "grow", href: `#/ex/${ex.id}` }, ex.title),
    kindBadge(ex.kind),
    ...(ex.serves || []).map((c) => tip(h("span", { class: "badge" }, c), COMPETENCY[c] || "")),
    statusLine(ex.status, ex.kind));
  for (const group of ["Read", "Build", "Catch", "Defend"]) {
    const here = s.exercises.filter((ex) => ex.group === group);
    if (!here.length) continue;
    const core = here.filter((ex) => ex.required), extra = here.filter((ex) => !ex.required);
    main.append(h("h2", {}, tip(h("span", {}, group), GROUP_INFO[group])), ...core.map(row));
    if (extra.length) main.append(h("details", {}, h("summary", { class: "muted" }, `Extra practice (${extra.length})`), ...extra.map(row)));
  }
}

// ---------- exercise kinds added by the redesign ----------
// What if: a change is made to the code and the learner says what happens. The server runs the change to know.
function whatIfPanel(info, id, afterChange, locked) {
  const el = h("div", { class: "whatif" });
  const LABELS = { pass: "The tests still pass", fail: "The tests fail", same: "Same output", different: "Different output", crash: "It crashes" };
  function draw(state, results) {
    const picks = state.questions.map(() => null);
    el.replaceChildren();
    if (state.ok) { el.append(h("p", { class: "ok" }, "✓ What if: done.")); return; }
    el.append(h("p", { class: "muted" }, "What happens after this change? The app really runs it to find out."));
    const boxes = state.questions.map((q, i) => h("div", { class: "review" }, h("p", {}, h("strong", {}, `${i + 1}. `), md(q.change)),
      h("div", {}, ...state.choices.map((c) => h("label", { style: "margin-right:1rem" },
        h("input", { type: "radio", name: `w${id}${i}`, onchange: () => { picks[i] = c; } }), " " + LABELS[c])))));
    const note = h("div");
    el.append(...boxes, h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (e) => {
      if (picks.includes(null)) { note.replaceChildren(h("p", { class: "bad" }, "Answer every question.")); return; }
      e.target.disabled = true;
      try {
        const r = await api("/whatif/answer", { exercise_id: id, answers: picks });
        r.results.forEach((res, i) => boxes[i].append(h("p", { class: res.correct ? "ok" : "bad" },
          (res.correct ? "✓ " : `✗ it was: ${LABELS[res.answer]}. `) + (res.result || ""))));
        note.replaceChildren(h("p", {}, r.ok ? "✓ All right." : "Not all right. Read the answers above, then try the new questions."));
        afterChange(r);
        if (!r.ok) setTimeout(() => draw(r.whatif), 2500);
        else draw(r.whatif);
      } catch (err) { note.replaceChildren(h("p", { class: "bad" }, err.message)); e.target.disabled = false; }
    } }, "Check my answers")), note);
  }
  draw(info);
  return el;
}

// Reading exercises: What if rounds, then (level 2) one sentence on the trap or (level 3) a fix and an explanation.
function readView(ex, id, afterChange) {
  const reviewSlot = h("div"), whatSlot = h("div"), outBox = h("pre", { hidden: "" }), later = h("div");
  const showOut = (t) => { outBox.hidden = false; outBox.textContent = "What the original prints:\n" + t; };
  if (ex.expected) showOut(ex.expected);
  const snippet = h("div");
  const cm = CodeMirror(snippet, { value: ex.snippet, mode: "python", lineNumbers: true, readOnly: true });
  setTimeout(() => cm.refresh(), 0);
  const answer = h("textarea", { placeholder: ex.level === 2 ? "One sentence." : "Answer the questions in your own words." });
  const written = ex.level >= 2 ? h("div", {}, h("h2", {}, ex.level === 2 ? "2. Name the trap" : "3. Explain it"),
    h("ol", {}, ex.questions.map((q) => h("li", {}, q))), answer,
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (e) => {
      e.target.disabled = true; e.target.textContent = "Reviewing, please wait...";
      try { showReview(await api("/review", { exercise_id: id, text: answer.value })); }
      catch (err) { reviewSlot.replaceChildren(h("pre", { class: "bad" }, String(err))); }
      e.target.disabled = false; e.target.textContent = "Submit for review";
    } }, "Submit for review")), reviewSlot) : null;
  const fixMsg = h("div"), fixOut = h("pre"), fixHolder = h("div");
  let fixCm = null;
  const fix = ex.level >= 3 ? h("div", {}, h("h2", {}, "2. Fix it"), md(ex.fix), fixHolder,
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: async () => {
      const r = await api("/fix", { exercise_id: id, code: fixCm.getValue() });
      fixOut.textContent = r.output;
      fixMsg.replaceChildren(h("p", { class: r.passed ? "ok" : "bad" }, r.passed ? "✓ It prints the target." : "✗ Not the target output yet."));
      afterChange(r.status);
    } }, "Run and check")), fixMsg, fixOut) : null;
  function openLater() {
    later.replaceChildren(...[fix, written].filter(Boolean));
    if (fix && !fixCm) { fixCm = editor(fixHolder, "python", ex.snippet); setTimeout(() => fixCm.refresh(), 0); }
  }
  main.append(h("h2", {}, "Read this code"), snippet, h("h2", {}, "1. What if?"), whatSlot, outBox, later);
  function wire(info) {
    whatSlot.replaceChildren(whatIfPanel(info, id, (r) => { afterChange(r.status); if (r.ok) { api(`/exercise/${id}`).then((x) => x.expected && showOut(x.expected)); openLater(); } }));
  }
  api("/whatif/start", { exercise_id: id }).then((r) => { wire(r.whatif); if (r.whatif.ok) openLater(); });
  function showReview(rev) {
    reviewSlot.replaceChildren(reviewBox(rev, async () => showReview(await api(`/reviews/${rev.review_id}/retry`, {}))) || "");
    if (rev && rev.status === "done") afterChange();
  }
  showReview(ex.review);
  return reviewSlot;
}

function triageView(ex, id, afterChange) {
  const picks = ex.proposals.map(() => ({ choice: null, reason: "" }));
  const out = h("div");
  const boxes = ex.proposals.map((p, i) => {
    const reason = h("input", { type: "text", placeholder: "Why? One sentence.", oninput: (e) => { picks[i].reason = e.target.value; } });
    const radios = ["accept", "reject"].map((c) => h("label", { style: "margin-right:1rem" },
      h("input", { type: "radio", name: `p${i}`, onchange: () => { picks[i].choice = c; } }), " " + c));
    return h("div", { class: "review" }, h("p", {}, h("strong", {}, `${i + 1}. ${p.title}`)), h("pre", {}, p.code), h("div", {}, ...radios), reason,
      DEV && p.correct ? h("p", { class: "ok" }, `Right call: ${p.correct}. ${p.why}`) : null);
  });
  main.append(...boxes, h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (e) => {
    if (picks.some((x) => !x.choice)) { out.replaceChildren(h("p", { class: "bad" }, "Decide on every change.")); return; }
    e.target.disabled = true;
    try {
      const r = await api("/triage", { exercise_id: id, decisions: picks.map((x) => ({ choice: x.choice, reason: x.reason })) });
      r.results.forEach((res, i) => boxes[i].append(h("p", { class: res.correct ? "ok" : "bad" },
        (res.correct ? "✓ " : `✗ the right call was ${res.key}. `) + res.why)));
      out.replaceChildren(h("p", {}, `${r.correct}/${r.total} right. ` + (r.passed ? "Passed." : "Not yet: read the reasons, then retry.")),
        r.review ? reviewBox(r.review, null) : h("p", { class: "muted" }, "Fill in a reason for every change to get the AI review of your reasoning (needed to finish)."));
      afterChange(r.status);
    } catch (err) { out.replaceChildren(h("p", { class: "bad" }, err.message)); }
    e.target.disabled = false;
  } }, "Submit decisions")), out);
}

// name-the-bug box: shown once the learner's fix passes
function bugPanel(ex, id, afterChange) {
  const slot = h("div"), box = h("textarea", { placeholder: "In one sentence: what was the bug, where, and what did it cause?" });
  const btn = h("button", { class: "primary", onclick: async (e) => {
    e.target.disabled = true;
    try {
      const rev = await api("/bug", { exercise_id: id, text: box.value });
      slot.replaceChildren(reviewBox(rev, null)); afterChange();
    } catch (err) { slot.replaceChildren(h("p", { class: "bad" }, err.message)); }
    e.target.disabled = false;
  } }, "Submit for review");
  return h("div", { class: "notice" }, h("strong", {}, "Name the bug. "), "Once the tests pass, say in one sentence what was wrong. This is what you would tell a teammate.", box, h("div", { class: "bar" }, btn), slot);
}

// The control check after a core build passes. Level 1: What if. Level 2: What if, then a change by hand.
// Level 3: explain two of your own lines, then a change by hand. The assistant is locked until it is done.
function controlPanel(ex, id, ctx, afterChange) {
  const el = h("div", { class: "notice" });
  const level = ex.control.level;
  async function call(path, body) { const r = await api(path, { exercise_id: id, ...body }); if (r.status) afterChange(r.status); if (ctx.assistantEl) ctx.assistantEl.refresh(); return r; }
  let last = "";
  const INTRO = { 1: "Show that you understand your code: say what happens when one line is changed.",
    2: "Show that you control your code: say what happens when one line is changed, then make one small change by hand.",
    3: "Prove that you control this code. I pick two lines of your passing solution for you to explain, then you make one small change by hand." };
  function changeBox(info) {
    const holder = h("div"), out = h("pre");
    const cm = editor(holder, ex.kind, last);
    cm.on("change", () => { last = cm.getValue(); });
    setTimeout(() => cm.refresh(), 0);
    return [h("h3", {}, level === 3 ? "B. Make this change by hand" : "2. Make this change by hand"), md(info.change), holder,
      h("div", { class: "bar" }, h("button", { class: info.b_ok ? "" : "primary", onclick: async () => {
        const r = await call("/control/change", { code: cm.getValue() }); results(out, r); draw(r.control, cm.getValue()); el.append(out);
      } }, info.b_ok ? "✓ Passed (run again)" : "Run the change tests"),
        h("span", { class: "muted" }, "The assistant is locked until this is done.")), out];
  }
  function draw(info, code) {
    if (code) last = code;
    el.replaceChildren(h("strong", {}, "Control check. "));
    if (info.complete) { el.append(h("span", { class: "ok" }, "✓ Done.")); return; }
    if (!info.started) {
      const startBtn = h("button", { class: "primary", onclick: async () => {
        const r = await call("/control/start", {}); draw(r.control, r.code);
      } }, "Start control check");
      if (!info.ready) startBtn.setAttribute("disabled", "");
      if (DEV && info.change) el.append(h("p", { class: "muted" }, "Dev mode: the change you would be asked to make is"), md(info.change));
      el.append(INTRO[level], h("div", { class: "bar" }, startBtn, info.ready ? null : h("span", { class: "muted" }, "Pass the tests first.")));
      return;
    }
    if (level < 3) {
      el.append(h("h3", {}, level === 2 ? "1. What if?" : "What if?"),
        whatIfPanel(info.whatif, id, (r) => { afterChange(r.status); if (ctx.assistantEl) ctx.assistantEl.refresh(); if (r.ok) draw(r.control); }));
      if (level === 2 && info.whatif_ok) el.append(...changeBox(info));
      return;
    }
    const expl = info.lines.map(() => h("textarea", { placeholder: "What does this line do, and why is it there?" }));
    const revSlot = h("div");
    el.append(h("h3", {}, "A. Explain these two lines of your code"),
      ...info.lines.flatMap((l, i) => [h("pre", {}, `${l.no}: ${l.text}`), expl[i]]),
      h("div", { class: "bar" }, h("button", { class: info.a_ok ? "" : "primary", onclick: async (e) => {
        e.target.disabled = true;
        try { const r = await call("/control/explain", { explanations: expl.map((x) => x.value) }); revSlot.replaceChildren(reviewBox(r.review, null)); draw(r.control, code); el.append(revSlot); }
        catch (err) { revSlot.replaceChildren(h("p", { class: "bad" }, err.message)); }
        e.target.disabled = false;
      } }, info.a_ok ? "✓ Explained (check again)" : "Check my explanations")), revSlot, ...changeBox(info));
  }
  (async () => {
    const info = ex.control;
    if (info.started && !info.complete) { const r = await api("/control/start", { exercise_id: id }); draw(r.control, r.code); }
    else draw(info, "");
  })();
  el.redraw = async () => { const fresh = (await api(`/exercise/${id}`)).control; if (!fresh.started || fresh.complete) draw(fresh, ""); };
  return el;
}

// An extra (not core) build where the assistant wrote code: a What if round shows the learner understood it.
function assistWhatIf(ex, id, afterChange) {
  const el = h("div", { class: "notice" });
  async function open() {
    const r = await api("/whatif/start", { exercise_id: id });
    el.replaceChildren(h("strong", {}, "What if. "), "The assistant wrote code for this exercise, so it only counts once you show you understand it.",
      whatIfPanel(r.whatif, id, (x) => afterChange(x.status)));
  }
  el.redraw = (st) => {
    if (DEV || !st.assisted || st.explain === true) { el.replaceChildren(); return; }
    if (el.querySelector(".whatif")) return;
    el.replaceChildren(h("strong", {}, "What if. "), "The assistant wrote code for this exercise, so it only counts once you show you understand it. ",
      h("button", { class: "primary", disabled: st.tests ? undefined : "", onclick: open }, "Start"),
      st.tests ? null : h("span", { class: "muted" }, " Pass the tests first."));
  };
  return el;
}

async function exView(id, mode = "blank") {
  const ex = await api(`/exercise/${id}?mode=${mode}`);
  const coded = ex.modes.length > 0;
  const back = h("p", {}, h("a", { href: `#/step/${ex.step_id}` }, "← Back to the step"));
  main.append(back, h("h1", {}, ex.title, " ", kindBadge(ex.kind)));
  const ctx = { getCode: () => "", getOutput: () => "", getLine: () => "", onAssisted: () => {}, grade: ex.grade_prompts };
  const statusEl = h("span", {});
  let applyStatus = (st) => { statusEl.replaceChildren(statusLine(st, ex.kind)); };
  const refreshStatus = async () => applyStatus((await api(`/exercise/${id}?mode=${mode}`)).status);
  const after = (st) => { if (st) applyStatus(st); else refreshStatus(); };
  ctx.onGraded = refreshStatus;
  helpSidebar(ex, ctx);
  if (ex.kind === "quiz") { main.append(md(ex.prompt)); return quizView(ex); }
  main.append(md(ex.prompt));
  if (ex.schema) main.append(h("details", {}, h("summary", {}, "Tables"), h("pre", {}, ex.schema)));
  if (ex.docs) main.append(h("details", { open: "" }, h("summary", {}, "Documentation (you may consult it, like in the interview)"), md(ex.docs)));
  const progress = DEV ? h("span") : h("div", { class: "bar" }, h("span", { class: "muted" }, "Progress (hover a tick):"), statusEl);
  applyStatus(ex.status);

  const reviewSlot = h("div");
  const extras = h("div");
  const nextSlot = h("div");
  nextSlot.replaceChildren(nextBar(ex, false));
  const refreshExtras = async () => extras.replaceChildren(extrasPanel(await api(`/exercise/${id}?mode=${mode}`)));
  refreshExtras();
  const showReview = (rev) => {
    reviewSlot.replaceChildren(reviewBox(rev, async () => {
      showReview(await api(`/reviews/${rev.review_id}/retry`, {}));
    }) || "");
    if (rev && rev.status === "done") { refreshExtras(); refreshStatus(); nextSlot.replaceChildren(nextBar(ex, true)); }
  };

  const finished = async (st) => {
    const now = st || (await api(`/exercise/${id}`)).status;
    applyStatus(now); refreshExtras(); nextSlot.replaceChildren(nextBar(ex, now.done));
  };
  if (ex.kind === "read") {
    main.append(progress);
    readView(ex, id, finished);
    main.append(nextSlot, extras);
    return;
  }
  if (ex.kind === "triage") {
    main.append(progress);
    triageView(ex, id, finished);
    main.append(nextSlot, extras);
    return;
  }
  const PLAIN = coded
    ? "Optional: explain your code as you would to the interviewer. It is sent with the AI review." : "Type your answer here, then press the button below.";
  const text = h("textarea", { placeholder: PLAIN });
  ctx.getCode = () => text.value;

  if (!coded) {
    main.append(progress, text, h("div", { class: "bar" }, tip(h("button", { class: "primary", onclick: async (e) => {
      e.target.disabled = true;
      e.target.textContent = "Reviewing, please wait...";
      try { showReview(await api("/review", { exercise_id: id, text: text.value })); }
      catch (err) { reviewSlot.replaceChildren(h("pre", { class: "bad" }, String(err))); }
      e.target.textContent = "Submit for review";
      e.target.disabled = false;
    } }, "Submit for review"), "An AI interviewer scores your answer 1 to 5 on each criterion and gives feedback. Takes a few seconds.")), reviewSlot, nextSlot, extras);
    showReview(ex.review);
    return;
  }

  const assistWhat = !ex.control && ex.whatif.needed !== undefined ? assistWhatIf(ex, id, after) : null;
  applyStatus = (st) => {
    statusEl.replaceChildren(statusLine(st, ex.kind));
    if (assistWhat) assistWhat.redraw(st);
    if (st.tests && bugSlot && ex.name_bug && !bugSlot.firstChild) bugSlot.append(bugPanel(ex, id, refreshStatus));
    if (controlEl && st.tests) controlEl.redraw();
  };
  const clock = h("span", { class: "timer" });
  const bugSlot = h("div");
  const controlEl = ex.control ? controlPanel(ex, id, ctx, after) : null;
  const challenge = mode === "challenge";
  const modeBar = h("div", { class: "bar" },
    tip(h("button", { onclick: () => render(() => exView(id, challenge ? "blank" : "challenge")) },
      challenge ? "Back to the starter code" : "Challenge: empty editor"),
      "Optional hard mode: start from an empty editor. It counts like any pass but never blocks you."),
    tip(clock, "Elapsed time. There is no limit."),
    ex.plan_required ? tip(h("span", { class: "chip todo" }, `plan: ${ex.plan_required}+ comment lines`),
      "Write your plan as # comment lines in the editor first. Submit is refused without it.") : null,
    ex.assistant === "off" ? tip(h("span", { class: "chip todo" }, "assistant off"), "Fix this one yourself.") : null);
  main.append(modeBar, progress);

  const holder = h("div");
  const out = h("pre");
  const reviewBtn = tip(h("button", { disabled: "" }, "Get AI review of my passing code"),
    "An AI interviewer reviews your last passing submission. Pass the tests first.");
  let cm = null, elapsed = () => 0, lastPassed = null;
  ctx.getCode = () => (cm ? cm.getValue() : "");
  ctx.getOutput = () => out.textContent;
  ctx.getLine = () => (cm ? cm.getLine(cm.getCursor().line).trim() : "");
  ctx.onAssisted = refreshStatus;
  applyStatus(ex.status);

  const draftKey = `draft:${id}:${mode}`;
  const readDraft = () => { try { return localStorage.getItem(draftKey); } catch (e) { return null; } };
  const writeDraft = (v) => { try { if (v === null) localStorage.removeItem(draftKey); else localStorage.setItem(draftKey, v); } catch (e) { /* drafts are a convenience only */ } };
  const saved = readDraft();
  cm = editor(holder, ex.kind, saved === null ? ex.code : saved);
  cm.on("change", () => writeDraft(cm.getValue()));
  setTimeout(() => cm.refresh(), 0); // an editor built before it is on the page draws blank until refreshed
  elapsed = startTimer(clock, 0);

  reviewBtn.addEventListener("click", async () => {
    reviewBtn.disabled = true;
    const label = reviewBtn.textContent;
    reviewBtn.textContent = "Reviewing, please wait...";
    try { showReview(await api("/review", { exercise_id: id, attempt_id: lastPassed, text: text.value })); }
    catch (e) { reviewSlot.replaceChildren(h("pre", { class: "bad" }, String(e))); }
    reviewBtn.textContent = label;
    reviewBtn.disabled = false;
  });
  main.append(holder, h("div", { class: "bar" },
    tip(h("button", { onclick: async () => cm && results(out, await api("/run", { exercise_id: id, code: cm.getValue() }), "run") },
      "Run"), "Runs your code as a script so you can try it with print(...). Nothing is recorded. Submit runs the hidden tests."),
    tip(h("button", { onclick: () => {
      if (!cm) return;
      if (cm.getValue() !== ex.code && !confirm("Replace your code with the starter?")) return;
      cm.setValue(ex.code); writeDraft(null); out.textContent = "";
    } }, "Reset code"), "Put the editor back to how this exercise started. Your typed code is replaced."),
    tip(h("button", { class: "primary", onclick: async () => {
      if (!cm) return;
      const r = await api("/submit", { exercise_id: id, code: cm.getValue(), mode, duration_s: elapsed() });
      results(out, r);
      applyStatus(r.status);
      if (r.passed) { lastPassed = r.attempt_id; reviewBtn.disabled = false; refreshExtras(); nextSlot.replaceChildren(nextBar(ex, true)); }
    } }, "Submit"), "Run the hidden tests and record the attempt. A pass counts toward the step.")), nextSlot, h("h2", {}, "Results"), out,
    bugSlot, controlEl, assistWhat, text, h("div", { class: "bar" }, reviewBtn), reviewSlot, extras);
  if (ex.status.tests && ex.name_bug) bugSlot.append(bugPanel(ex, id, refreshStatus));
  showReview(ex.review);
}

async function cardsView() {
  const due = await api("/cards/due");
  main.append(h("h1", {}, "Warm-up cards"),
    h("p", { class: "muted" }, "Look at the card, say or type your answer, then press Flip to check. Cards you miss come back today; cards you get right come back after 1, 2, 4, 8, then 16 days."));
  if (!due.length) { main.append(h("p", {}, "Nothing due. Come back tomorrow.")); return; }
  const card = due[0];
  const back = h("pre", { hidden: "" }, card.back);
  const grade = async (correct) => { await api("/cards/grade", { card_id: card.id, correct }); route(); };
  const buttons = h("div", { class: "bar", hidden: "" },
    h("button", { onclick: () => grade(true) }, "Got it"),
    h("button", { onclick: () => grade(false) }, "Missed it"));
  main.append(h("p", { class: "muted" }, `${due.length} due`), md(card.front),
    h("textarea", { placeholder: "Your answer (optional), then flip." }),
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: () => { back.hidden = false; buttons.hidden = false; } }, "Flip")),
    back, buttons);
}

async function mockView() {
  main.append(h("h1", {}, "Mock round"),
    h("p", {}, "Two Python tasks with the assistant on, 35 minutes. Then two 'explain this line' questions about your own code and three follow-up questions. The clock starts when you press Start. Score out of 100: hidden tests 35%, AI review 25%, finishing in time 10%, small asks 10%, running code before accepting the assistant's code 10%, explaining your lines 10%."));
  main.append(h("button", { class: "primary", onclick: async () => {
    const m = await api("/mock/start", {});
    const scope = `mock:${m.mock_id}`;
    main.replaceChildren();
    const clock = h("span", { class: "timer" });
    const elapsed = startTimer(clock, m.time_limit_s);
    main.append(h("div", { class: "bar" }, h("strong", {}, "Mock round"), clock));
    const editors = m.tasks.map((t, i) => {
      const holder = h("div"), out = h("pre");
      main.append(h("h2", {}, `Task ${i + 1}: ${t.title}`), md(t.prompt),
        t.docs ? h("details", { open: "" }, h("summary", {}, "Documentation"), md(t.docs)) : null, holder,
        h("div", { class: "bar" }, h("button", { onclick: async () => results(out, await api("/run", { exercise_id: t.id, code: cm.getValue(), scope }), "run") }, "Run")), out);
      const cm = editor(holder, "python", t.code);
      setTimeout(() => cm.refresh(), 0);
      return cm;
    });
    sidebarTabs([{ id: "assistant", label: "Assistant", el: assistantPanel(scope, {
      getCode: () => editors.map((e, i) => `# TASK ${i + 1}\n${e.getValue()}`).join("\n\n"), getOutput: () => "",
      getLine: () => { const e = editors.find((x) => x.hasFocus()) || editors[0]; return e.getLine(e.getCursor().line).trim(); },
      onAssisted: () => {}, grade: true }) }]);
    main.append(h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (e) => {
      e.target.disabled = true;
      const r = await api(`/mock/${m.mock_id}/submit`, { codes: editors.map((x) => x.getValue()), duration_s: elapsed() });
      clearInterval(tick);
      const outs = r.results.map((res, i) => { const o = h("pre"); results(o, res); return [h("h2", {}, `Task ${i + 1} result`), o]; });
      const lineAnswers = r.lines.map(() => h("textarea"));
      const answers = r.questions.map(() => h("textarea"));
      main.replaceChildren(h("h1", {}, "Follow-up questions"), ...outs.flat(),
        h("h2", {}, "Explain these lines of your code"),
        ...r.lines.flatMap((l, i) => [h("pre", {}, `Task ${l.task + 1}, line ${l.no}: ${l.text}`), lineAnswers[i]]),
        h("h2", {}, "Questions"),
        ...r.questions.flatMap((q, i) => [h("p", {}, h("strong", {}, q)), answers[i]]),
        h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (ev) => {
          ev.target.disabled = true;
          const done = await api(`/mock/${m.mock_id}/answers`, { answers: answers.map((a) => a.value), line_answers: lineAnswers.map((a) => a.value) });
          const sc = done.score, pc = (x) => Math.round(x * 100) + "%";
          main.replaceChildren(h("h1", {}, `Score: ${sc.total}/100`),
            h("p", {}, `Tests passed: ${pc(sc.pass_rate)}. Review average: ${sc.review_avg.toFixed(1)}/5. ${sc.in_time ? "Inside" : "Over"} the time limit. ` +
              `Small asks: ${pc(sc.asks)}. Ran code before accepting: ${pc(sc.ran)}. Line explanations: ${pc(sc.lines)}. ` +
              (done.readiness === null ? "" : `Readiness estimate: ${done.readiness}/100.`)),
            ...done.reviews.map((rev) => reviewBox(rev, null)));
        } }, "Submit answers")));
    } }, "Finish coding")));
  } }, "Start"));
}

async function render(view) {
  clearInterval(tick);
  hideHelp();
  main.replaceChildren();
  try { await view(); } catch (e) { main.append(h("pre", { class: "bad" }, String(e))); }
}

function route() {
  const [, name, id] = location.hash.split("/");
  const section = name === "step" || name === "ex" ? "" : (name || "");
  document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("active", a.dataset.route === section));
  if (name === "step") render(() => stepView(id));
  else if (name === "ex") render(() => exView(id));
  else if (name === "cards") render(cardsView);
  else if (name === "mock") render(mockView);
  else if (name === "kb") render(() => kbView(id));
  else render(journeyView);
}

fetch("/api/version").then((r) => r.json()).then((v) => {
  const el = document.getElementById("version");
  el.textContent = "version " + v.version;
  el.title = "Running from " + v.path;
}).catch(() => {});

async function setupProvider() {
  const sel = document.getElementById("provider");
  const draw = (s) => {
    sel.replaceChildren(...s.providers.map((p) => h("option",
      { value: p.id, ...(p.configured ? {} : { disabled: "" }), ...(p.id === s.provider ? { selected: "" } : {}) },
      `${p.label} · ${p.model}${p.configured ? "" : " (no key in .env)"}`)));
  };
  try {
    draw(await api("/settings"));
    sel.addEventListener("change", async () => {
      try { draw(await api("/settings", { provider: sel.value })); }
      catch (e) { alert(e.message); draw(await api("/settings")); }
    });
  } catch (e) { sel.parentElement.hidden = true; }
}
setupProvider();

document.getElementById("theme-toggle").addEventListener("click", () => {
  const root = document.documentElement;
  const dark = root.getAttribute("data-theme") === "dark" ||
    (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
  const next = dark ? "light" : "dark";
  root.setAttribute("data-theme", next);
  try { localStorage.setItem("theme", next); } catch (e) { /* not remembered in private mode */ }
});

const devBtn = document.getElementById("dev-toggle");
function drawDev(state) {
  DEV = state.dev;
  document.body.classList.toggle("dev", DEV);
  devBtn.classList.toggle("active", DEV);
  devBtn.textContent = DEV ? "Dev: on" : "Dev";
  devBtn.disabled = state.forced;
  devBtn.title = state.forced ? "Dev mode is forced on by GYM_DEV=1" : "Dev mode: open every step, show all answers, hide progress";
}
devBtn.addEventListener("click", async () => { drawDev(await api("/dev", { dev: !DEV })); route(); });

window.addEventListener("hashchange", route);
api("/dev").then(drawDev).catch(() => {}).finally(route);

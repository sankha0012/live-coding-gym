const main = document.getElementById("main");
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

const KIND_INFO = {
  python: ["Python", "Write a function in Python. Hidden tests check it, like Coderbyte."],
  sql: ["SQL", "Write a SQL query. Its result is compared with a reference result."],
  tests: ["Write tests", "Write pytest tests. They must pass on the correct code and fail on every buggy version."],
  quiz: ["Quiz", "Multiple choice, graded instantly. Wrong answers come with an explanation."],
  open: ["Open question", "Answer in your own words. An AI interviewer scores it against a rubric."],
  prompt: ["Prompt", "Write the prompt you would give an AI assistant. An AI interviewer scores the prompt."],
  explain: ["Explain code", "Explain the code as you would to the interviewer. An AI interviewer scores it."],
};
const MODE_INFO = {
  retype: "Study the solution, then hide it and type it from memory.",
  gaps: "Fill in the blanks (____) of a half-written solution.",
  blank: "Start from the bare function. Passing the hidden tests here counts toward the step.",
  timed: "Same as blank, against the clock. Optional extra practice for interview pace.",
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
  tests: "Hidden tests: passed once in blank or timed mode.",
  timed: "Passed within the time limit (in timed mode).",
  review: "AI review: every criterion at or above the step's minimum score.",
  explain: "The assistant wrote code for this exercise, so you must explain it in your own words and pass the AI review.",
  assisted: "You asked the assistant to write code for this exercise.",
};

function statusLine(st) {
  const chip = (key, label) => (st[key] === null ? null
    : tip(h("span", { class: "chip " + (st[key] ? "done" : "todo") }, label, " ", mark(st[key])), CHIP_INFO[key]));
  return h("span", {}, chip("tests", "tests"), chip("timed", "timed"), chip("review", "AI review"),
    chip("explain", "explain it back"),
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
      h("input", { type: "radio", name: `q${i}`, onchange: () => { picks[i] = j; } }), " " + o))));
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

const MODE_NOTE = {
  tutor: "Tutor: explains, gives hints and reviews your code, but never writes the solution. Steps 1 to 3 train writing code by hand, so this is the only mode there.",
  interview: "Interview: behaves like the assistant allowed in the real interview and writes code when you ask. The interviewer judges your prompts. If it writes code for you, you must explain that code to pass this exercise.",
};
const QUICK = [
  ["Explain the task", "Explain this task in plain words and tell me what to think about first. Do not give the solution."],
  ["Give me a hint", "Give me one hint to get unstuck, without giving the answer."],
  ["Why does my code fail?", "My code fails or gives a wrong result. Look at my code and the last output, point at the likely problem and explain why, but do not rewrite it for me."],
  ["Review my code", "Review my current code for correctness, edge cases and readability. List the problems; do not rewrite it."],
];

// The assistant chat. ctx = { getCode(), getOutput(), onAssisted() } gives it the learner's current state.
function assistantPanel(scope, ctx) {
  const list = h("div", { class: "chat-list" });
  const note = h("p", { class: "muted chat-note" });
  const quick = h("div", { class: "chat-quick" });
  const gradeSlot = h("div");
  const error = h("p", { class: "bad" });
  const input = h("textarea", { class: "chat-input", rows: "3",
    placeholder: "Ask the assistant. Enter sends, Shift+Enter adds a line." });
  const modeSel = h("select", { onchange: () => draw() },
    h("option", { value: "tutor" }, "Tutor"), h("option", { value: "interview" }, "Interview"));
  const gradeBtn = tip(h("button", { onclick: async () => {
    gradeBtn.disabled = true;
    try { const rev = await api("/chat/grade", { scope }); gradeSlot.replaceChildren(reviewBox(rev, null)); }
    catch (e) { gradeSlot.replaceChildren(h("p", { class: "bad" }, e.message)); }
    gradeBtn.disabled = false;
  } }, "Grade my prompts"), "An AI interviewer scores the prompts you typed here: clarity, constraints, edge cases, whether you stay in control.");
  const clearBtn = tip(h("button", { onclick: async () => {
    if (!confirm("Clear this chat? (It will not undo the 'assisted' mark on this exercise.)")) return;
    await api("/chat/clear", { scope }); await load();
  } }, "Clear chat"), "Delete this conversation.");
  let state = { messages: [], interview_allowed: false };
  const mode = () => (modeSel.value === "interview" && state.interview_allowed ? "interview" : "tutor");

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
    modeSel.querySelector('option[value="interview"]').disabled = !state.interview_allowed;
    if (!state.interview_allowed) modeSel.value = "tutor";
    note.textContent = MODE_NOTE[mode()];
    list.replaceChildren(...(state.messages.length ? state.messages.map((m) => {
      const box = m.role === "user" ? h("div", { class: "msg user" }, m.content) : h("div", { class: "msg assistant" }, md(m.content));
      if (m.role !== "user") decorate(box);
      return box;
    }) : [h("p", { class: "muted" }, mode() === "tutor"
      ? "Ask about the task, a concept or an error. Or use a quick button below."
      : "Write your prompt as you would in the interview: task, inputs and outputs, constraints, edge cases.")]));
    list.scrollTop = list.scrollHeight;
    quick.replaceChildren(...(mode() === "tutor" ? QUICK.map(([label, text]) => h("button", { onclick: () => send(text) }, label)) : []));
    gradeBtn.hidden = !(mode() === "interview" && state.messages.some((m) => m.role === "user"));
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
      const r = await api("/chat", { scope, message: text, mode: mode(), code: ctx.getCode(), output: ctx.getOutput() });
      const wasAssisted = state.assisted;
      state = { ...state, messages: r.messages, assisted: r.assisted, interview_allowed: r.interview_allowed };
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
    try { state = await api(`/chat?scope=${encodeURIComponent(scope)}`); if (state.interview_allowed) modeSel.value = "interview"; }
    catch (e) { error.textContent = e.message; }
    draw();
  }
  const el = h("div", { class: "chat" },
    h("div", { class: "bar" }, tip(h("span", {}, "Mode"), "Tutor teaches and hints. Interview works like the assistant in the real interview."), modeSel, clearBtn),
    note, list, error, quick, input,
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: () => send() }, "Send"), gradeBtn), gradeSlot);
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
  if (ex.kind !== "quiz") panes.push({ id: "assistant", label: "Assistant", el: assistantPanel(ex.id, ctx) });
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

async function journeyView() {
  const j = await api("/journey");
  main.append(h("h1", {}, "Your journey"),
    h("p", { class: "muted" }, "Work from the top. Each step opens when you finish most of the previous one. Stuck or short on time? You can unlock any step yourself."));
  if (j.errors.length) main.append(h("pre", { class: "bad" }, "Broken content:\n" + j.errors.join("\n")));
  main.append(j.next
    ? h("div", { class: "bar" }, tip(h("a", { class: "button", href: `#/ex/${j.next.exercise_id}` }, "Continue: " + j.next.title),
        "Jumps to the next unfinished exercise, in " + j.next.step_title))
    : h("p", {}, "Every step is done. Run a mock round to test yourself."));
  main.append(h("p", {},
    tip(h("span", {}, j.readiness === null ? "Readiness: not yet measured" : `Readiness: ${j.readiness}/100`),
      "Average score of your last three mock rounds. It is an estimate, not a promise."),
    "   ", h("a", { href: "#/cards" }, `Flashcards due today: ${j.due_cards}`)));
  for (const s of j.steps) {
    const pct = s.total ? Math.round(100 * s.done / s.total) : 0;
    const need = s.total ? Math.round(100 * s.needed / s.total) : 0;
    const bar = tip(h("div", { class: "progress" }, h("div", { class: "fill", style: `width:${pct}%` }),
      h("div", { class: "needed", style: `left:${need}%` })),
      s.total ? `${s.done} of ${s.total} done. The marker shows the ${s.needed} needed to pass.` : "No exercises here. This step is measured by mock rounds.");
    const label = s.passed ? tip(h("span", { class: "ok" }, "passed ✓"), "You finished enough of this step.")
      : s.total ? h("span", { class: "muted" }, `${s.done}/${s.total} (need ${s.needed})`) : h("span", { class: "muted" }, "mock rounds");
    const title = s.unlocked ? h("a", { href: `#/step/${s.id}` }, `${s.order}. ${s.title}`)
      : tip(h("span", {}, `🔒 ${s.order}. ${s.title}`), "Opens when you finish the step above, or unlock it yourself.");
    const row = h("div", { class: "row" + (s.unlocked ? "" : " locked") }, h("span", { class: "grow" }, title), bar, label);
    if (!s.unlocked) {
      row.append(tip(h("button", { onclick: async () => { await api("/unlock", { step_id: s.id }); route(); } }, "Unlock"),
        "Open this step now without finishing the previous one."));
    }
    main.append(row);
  }
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
  main.append(h("p", {}, h("a", { href: "#/" }, "← Journey")), h("h1", {}, s.title));
  if (g.total) {
    main.append(h("p", { class: "muted" },
      `Pass this step by finishing ${g.needed} of its ${g.total} required exercises (${g.done} done). ` +
      "Hover a badge or tick for what it means."));
  }
  if (s.lessons.length) main.append(h("h2", {}, "Read first"));
  for (const lesson of s.lessons) {
    main.append(h("details", {}, h("summary", {}, lesson.title), md(lesson.body)));
  }
  if (!s.exercises.length) {
    main.append(h("p", {}, "This step has no exercises. Practise with ", h("a", { href: "#/mock" }, "mock rounds"), "; your last three scores give the readiness estimate."));
    return;
  }
  main.append(h("h2", {}, "Exercises"));
  for (const ex of s.exercises) {
    main.append(h("div", { class: "row" },
      h("a", { class: "grow", href: `#/ex/${ex.id}` }, ex.title),
      kindBadge(ex.kind),
      ex.required ? null : tip(h("span", { class: "badge" }, "optional"), "Does not count toward passing the step."),
      statusLine(ex.status)));
  }
}

async function exView(id, mode = "blank") {
  const ex = await api(`/exercise/${id}?mode=${mode}`);
  const coded = ex.modes.length > 0;
  const back = h("p", {}, h("a", { href: `#/step/${ex.step_id}` }, "← Back to the step"));
  main.append(back, h("h1", {}, ex.title, " ", kindBadge(ex.kind)));
  const ctx = { getCode: () => "", getOutput: () => "", onAssisted: () => {} };
  helpSidebar(ex, ctx);
  if (ex.kind === "quiz") { main.append(md(ex.prompt)); return quizView(ex); }
  main.append(md(ex.prompt));
  if (ex.schema) main.append(h("details", {}, h("summary", {}, "Tables"), h("pre", {}, ex.schema)));

  const reviewSlot = h("div");
  const extras = h("div");
  const nextSlot = h("div");
  nextSlot.replaceChildren(nextBar(ex, false));
  const refreshExtras = async () => extras.replaceChildren(extrasPanel(await api(`/exercise/${id}?mode=${mode}`)));
  refreshExtras();
  let applyStatus = () => {};
  const refreshStatus = async () => applyStatus((await api(`/exercise/${id}?mode=${mode}`)).status);
  const showReview = (rev) => {
    reviewSlot.replaceChildren(reviewBox(rev, async () => {
      showReview(await api(`/reviews/${rev.review_id}/retry`, {}));
    }) || "");
    if (rev && rev.status === "done") { refreshExtras(); refreshStatus(); nextSlot.replaceChildren(nextBar(ex, true)); }
  };
  const PLAIN = coded
    ? "Optional: explain your code as you would to the interviewer. It is sent with the AI review." : "Type your answer here, then press the button below.";
  const text = h("textarea", { placeholder: PLAIN });
  ctx.getCode = () => text.value;

  if (!coded) {
    main.append(text, h("div", { class: "bar" }, tip(h("button", { class: "primary", onclick: async (e) => {
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

  const picker = h("select", { onchange: (e) => render(() => exView(id, e.target.value)) },
    ex.modes.map((m) => h("option", m === mode ? { value: m, selected: "" } : { value: m }, m)));
  const clock = h("span", { class: "timer" });
  const statusEl = h("span", {}, statusLine(ex.status));
  const assistNote = h("div");
  applyStatus = (st) => {
    statusEl.replaceChildren(statusLine(st));
    const needExplain = st.assisted && st.explain !== true;
    assistNote.replaceChildren(needExplain ? h("div", { class: "notice" }, h("strong", {}, "Explain it back. "),
      "The assistant wrote code for this exercise, so it only counts once you explain that code in your own words. Write your explanation in the box below the results, pass the tests, then press 'Get AI review'.") : "");
    text.placeholder = st.assisted
      ? "Required: explain, in your own words, what the code does, why it works and one edge case. The AI review grades this explanation." : PLAIN;
  };
  applyStatus(ex.status);
  const modeHelp = h("span", { class: "muted" }, MODE_INFO[mode] || "");
  main.append(assistNote, h("div", { class: "bar" }, tip(h("span", {}, "Mode"), "How you want to practise this exercise. Switching mode keeps your progress."),
      picker, tip(clock, "Elapsed time" + (mode === "timed" ? ` / limit (${fmt(ex.time_limit_s)})` : ". No limit in this mode."))),
    h("div", { class: "bar" }, modeHelp), h("div", { class: "bar" }, h("span", { class: "muted" }, "Progress (hover a tick):"), statusEl));

  const holder = h("div");
  const out = h("pre");
  const reviewBtn = tip(h("button", { disabled: "" }, "Get AI review of my passing code"),
    "An AI interviewer reviews your last passing submission. Pass the tests first.");
  let cm = null, elapsed = () => 0, lastPassed = null;
  ctx.getCode = () => (cm ? cm.getValue() : "");
  ctx.getOutput = () => out.textContent;
  ctx.onAssisted = refreshStatus;

  const draftKey = `draft:${id}:${mode}`;
  const readDraft = () => { try { return localStorage.getItem(draftKey); } catch (e) { return null; } };
  const writeDraft = (v) => { try { if (v === null) localStorage.removeItem(draftKey); else localStorage.setItem(draftKey, v); } catch (e) { /* drafts are a convenience only */ } };
  const begin = () => {
    holder.replaceChildren();
    const saved = readDraft();
    cm = editor(holder, ex.kind, saved === null ? ex.code : saved);
    cm.on("change", () => writeDraft(cm.getValue()));
    setTimeout(() => cm.refresh(), 0); // an editor built before it is on the page draws blank until refreshed
    elapsed = startTimer(clock, mode === "timed" ? ex.time_limit_s : 0);
  };
  if (mode === "retype") {
    holder.append(h("p", {}, "Read the solution until you can rebuild it, then hide it and type it from memory."),
      h("pre", {}, ex.solution), h("button", { onclick: begin }, "Hide and start"));
  } else begin();

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
    } }, "Submit"), "Run the hidden tests and record the attempt. A pass counts toward the step.")), nextSlot, h("h2", {}, "Results"), out, text, h("div", { class: "bar" }, reviewBtn), reviewSlot, extras);
  showReview(ex.review);
}

async function cardsView() {
  const due = await api("/cards/due");
  main.append(h("h1", {}, "Warm-up cards"),
    h("p", { class: "muted" }, "Read the task, type the answer from memory, then press Flip to check. Cards you miss come back today; cards you get right come back after 1, 2, 4, 8, then 16 days."));
  if (!due.length) { main.append(h("p", {}, "Nothing due. Come back tomorrow.")); return; }
  const card = due[0];
  const back = h("pre", { hidden: "" }, card.back);
  const grade = async (correct) => { await api("/cards/grade", { card_id: card.id, correct }); route(); };
  const buttons = h("div", { class: "bar", hidden: "" },
    h("button", { onclick: () => grade(true) }, "Got it"),
    h("button", { onclick: () => grade(false) }, "Missed it"));
  main.append(h("p", { class: "muted" }, `${due.length} due`), md(card.front),
    h("textarea", { placeholder: "Type it from memory, then flip." }),
    h("div", { class: "bar" }, h("button", { class: "primary", onclick: () => { back.hidden = false; buttons.hidden = false; } }, "Flip")),
    back, buttons);
}

async function mockView() {
  main.append(h("h1", {}, "Mock round"),
    h("p", {}, "One Python task, one SQL task, an AI assistant in the sidebar (your prompts to it are scored, like in the real interview), then three follow-up questions from an AI interviewer. 45 minutes. The clock starts when you press Start. Score out of 100: hidden tests 50%, AI review 40%, finishing in time 10%."));
  main.append(h("button", { class: "primary", onclick: async () => {
    const m = await api("/mock/start", {});
    main.replaceChildren();
    const clock = h("span", { class: "timer" });
    const elapsed = startTimer(clock, m.time_limit_s);
    const pyHolder = h("div"), sqlHolder = h("div");
    const prompt = h("textarea", { placeholder: "Optional. If you use the assistant in the sidebar, the prompts you type there are scored. If you do not, write here the prompt you would give an AI assistant for the Python task." });
    main.append(h("div", { class: "bar" }, h("strong", {}, "Mock round"), clock),
      h("h2", {}, "Python: " + m.python.title), md(m.python.prompt), pyHolder,
      h("h2", {}, "SQL: " + m.sql.title), md(m.sql.prompt), h("pre", {}, m.sql.schema), sqlHolder,
      h("h2", {}, "Your prompt for the AI assistant"), prompt);
    const py = editor(pyHolder, "python", m.python.code), sql = editor(sqlHolder, "sql", m.sql.code);
    sidebarTabs([{ id: "assistant", label: "Assistant", el: assistantPanel(`mock:${m.mock_id}`, {
      getCode: () => `# PYTHON\n${py.getValue()}\n\n-- SQL\n${sql.getValue()}`, getOutput: () => "", onAssisted: () => {} }) }]);
    main.append(h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (e) => {
      e.target.disabled = true;
      const r = await api(`/mock/${m.mock_id}/submit`, {
        python_code: py.getValue(), sql_code: sql.getValue(), prompt_text: prompt.value, duration_s: elapsed() });
      clearInterval(tick);
      const pyOut = h("pre"), sqlOut = h("pre");
      results(pyOut, r.python); results(sqlOut, r.sql);
      const answers = r.questions.map(() => h("textarea"));
      main.replaceChildren(h("h1", {}, "Follow-up questions"), h("h2", {}, "Python result"), pyOut,
        h("h2", {}, "SQL result"), sqlOut,
        ...r.questions.flatMap((q, i) => [h("p", {}, h("strong", {}, q)), answers[i]]),
        h("div", { class: "bar" }, h("button", { class: "primary", onclick: async (ev) => {
          ev.target.disabled = true;
          const done = await api(`/mock/${m.mock_id}/answers`, { answers: answers.map((a) => a.value) });
          main.replaceChildren(h("h1", {}, `Score: ${done.score.total}/100`),
            h("p", {}, `Tests passed: ${Math.round(done.score.pass_rate * 100)}%. Review average: ${done.score.review_avg.toFixed(1)}/5. ` +
              `${done.score.in_time ? "Inside" : "Over"} the time limit. ` +
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

window.addEventListener("hashchange", route);
route();

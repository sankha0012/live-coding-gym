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

function mark(value) {
  if (value === null) return null;
  return h("span", { class: value ? "ok" : "bad" }, value ? "✓" : "✗");
}

function statusLine(st) {
  const part = (label, v) => (v === null ? null : h("span", {}, label, " ", mark(v), "  "));
  return h("span", {}, part("tests", st.tests), part("timed", st.timed), part("review", st.review));
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
  if (ex.say) wrap.append(h("details", {}, h("summary", {}, "How to say it out loud"), md(ex.say)));
  if (ex.model_prompt) wrap.append(h("details", {}, h("summary", {}, "A good prompt for an AI assistant"), md(ex.model_prompt)));
  return wrap;
}

function quizView(ex) {
  const picks = ex.quiz.map(() => null);
  const note = h("div");
  const boxes = ex.quiz.map((q, i) => h("div", { class: "review" },
    h("p", {}, h("strong", {}, `${i + 1}. ${q.q}`)),
    q.options.map((o, j) => h("label", { style: "display:block" },
      h("input", { type: "radio", name: `q${i}`, onchange: () => { picks[i] = j; } }), " " + o))));
  main.append(...boxes, h("div", { class: "bar" },
    h("button", { onclick: async () => {
      if (picks.includes(null)) { note.replaceChildren(h("p", { class: "bad" }, "Answer every question.")); return; }
      const r = await api("/quiz", { exercise_id: ex.id, answers: picks });
      r.results.forEach((res, i) => boxes[i].append(h("p", { class: res.correct ? "ok" : "bad" },
        (res.correct ? "✓ " : `✗ right answer: ${ex.quiz[i].options[res.answer]}. `) + res.why)));
      note.replaceChildren(h("p", {}, `${r.correct}/${r.total}. ` +
        (r.passed ? "Passed." : "Not yet: read the explanations, then try again."),
        h("button", { onclick: route }, "Try again")));
    } }, "Submit answers")), note);
}

function results(out, r) {
  out.textContent = "";
  for (const t of r.tests) out.append(`${t.passed ? "PASS" : "FAIL"}  ${t.name}\n`);
  out.append((r.tests.length ? "\n" : "") + r.output);
}

async function journeyView() {
  const j = await api("/journey");
  main.append(h("h1", {}, "Your journey"));
  if (j.errors.length) main.append(h("pre", { class: "bad" }, "Broken content:\n" + j.errors.join("\n")));
  main.append(h("p", {},
    j.readiness === null ? "Readiness: finish three mock rounds to get an estimate."
      : `Readiness estimate: ${j.readiness}/100 (average of your last three mock rounds).`,
    `  Cards due today: ${j.due_cards}.`));
  for (const s of j.steps) {
    const row = h("div", { class: "row" + (s.unlocked ? "" : " locked") },
      h("span", { class: "grow" }, s.unlocked
        ? h("a", { href: `#/step/${s.id}` }, `${s.order}. ${s.title}`) : `${s.order}. ${s.title}`),
      h("span", { class: s.passed ? "ok" : "muted" }, s.passed ? "passed" : `${s.done}/${s.total}`));
    if (!s.unlocked) {
      row.append(h("button", { onclick: async () => { await api("/unlock", { step_id: s.id }); route(); } },
        "Unlock anyway"));
    }
    main.append(row);
  }
  if (j.mocks.length) {
    main.append(h("h2", {}, "Mock history"));
    for (const m of j.mocks) main.append(h("div", { class: "row" }, `${m.started_at}  score ${m.total}/100`));
  }
}

async function stepView(id) {
  const s = await api(`/step/${id}`);
  main.append(h("h1", {}, s.title));
  for (const lesson of s.lessons) {
    main.append(h("details", {}, h("summary", {}, lesson.title), md(lesson.body)));
  }
  main.append(h("h2", {}, "Exercises"));
  for (const ex of s.exercises) {
    main.append(h("div", { class: "row" },
      h("a", { class: "grow", href: `#/ex/${ex.id}` }, ex.title),
      h("span", { class: "muted" }, ex.kind + (ex.required ? "" : " (optional)")),
      statusLine(ex.status)));
  }
}

async function exView(id, mode = "blank") {
  const ex = await api(`/exercise/${id}?mode=${mode}`);
  const coded = ex.modes.length > 0;
  if (ex.kind === "quiz") { main.append(h("h1", {}, ex.title), md(ex.prompt)); return quizView(ex); }
  main.append(h("h1", {}, ex.title), md(ex.prompt));
  if (ex.schema) main.append(h("details", {}, h("summary", {}, "Tables"), h("pre", {}, ex.schema)));

  const reviewSlot = h("div");
  const extras = h("div");
  const refreshExtras = async () => extras.replaceChildren(extrasPanel(await api(`/exercise/${id}?mode=${mode}`)));
  refreshExtras();
  const showReview = (rev) => {
    reviewSlot.replaceChildren(reviewBox(rev, async () => {
      showReview(await api(`/reviews/${rev.review_id}/retry`, {}));
    }) || "");
    if (rev && rev.status === "done") refreshExtras();
  };
  const text = h("textarea", { placeholder: coded
    ? "Explain your code as you would to the interviewer (sent with the review)." : "Your answer" });

  if (!coded) {
    main.append(text, h("div", { class: "bar" }, h("button", { onclick: async (e) => {
      e.target.disabled = true;
      e.target.textContent = "Reviewing, please wait...";
      try { showReview(await api("/review", { exercise_id: id, text: text.value })); }
      catch (err) { reviewSlot.replaceChildren(h("pre", { class: "bad" }, String(err))); }
      e.target.textContent = "Submit for review";
      e.target.disabled = false;
    } }, "Submit for review")), reviewSlot, extras);
    showReview(ex.review);
    return;
  }

  const picker = h("select", { onchange: (e) => render(() => exView(id, e.target.value)) },
    ex.modes.map((m) => h("option", m === mode ? { value: m, selected: "" } : { value: m }, m)));
  const clock = h("span", { class: "timer" });
  const statusEl = h("span", {}, statusLine(ex.status));
  main.append(h("div", { class: "bar" }, "Mode ", picker, clock, statusEl));

  const holder = h("div");
  const out = h("pre");
  const reviewBtn = h("button", { disabled: "" }, "Get AI review of last passing submission");
  let cm = null, elapsed = () => 0, lastPassed = null;

  const begin = () => {
    holder.replaceChildren();
    cm = editor(holder, ex.kind, ex.code);
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
    h("button", { onclick: async () => cm && results(out, await api("/run", { exercise_id: id, code: cm.getValue() })) },
      "Run"),
    h("button", { onclick: async () => {
      if (!cm) return;
      const r = await api("/submit", { exercise_id: id, code: cm.getValue(), mode, duration_s: elapsed() });
      results(out, r);
      statusEl.replaceChildren(statusLine(r.status));
      if (r.passed) { lastPassed = r.attempt_id; reviewBtn.disabled = false; refreshExtras(); }
    } }, "Submit")), out, text, h("div", { class: "bar" }, reviewBtn), reviewSlot, extras);
  showReview(ex.review);
}

async function cardsView() {
  const due = await api("/cards/due");
  main.append(h("h1", {}, "Warm-up cards"));
  if (!due.length) { main.append(h("p", {}, "Nothing due. Come back tomorrow.")); return; }
  const card = due[0];
  const back = h("pre", { hidden: "" }, card.back);
  const grade = async (correct) => { await api("/cards/grade", { card_id: card.id, correct }); route(); };
  const buttons = h("div", { class: "bar", hidden: "" },
    h("button", { onclick: () => grade(true) }, "Got it"),
    h("button", { onclick: () => grade(false) }, "Missed it"));
  main.append(h("p", { class: "muted" }, `${due.length} due`), md(card.front),
    h("textarea", { placeholder: "Type it from memory, then flip." }),
    h("div", { class: "bar" }, h("button", { onclick: () => { back.hidden = false; buttons.hidden = false; } }, "Flip")),
    back, buttons);
}

async function mockView() {
  main.append(h("h1", {}, "Mock round"),
    h("p", {}, "One Python task, one SQL task, the prompt you would give an AI assistant, then follow-up questions. 45 minutes."));
  main.append(h("button", { onclick: async () => {
    const m = await api("/mock/start", {});
    main.replaceChildren();
    const clock = h("span", { class: "timer" });
    const elapsed = startTimer(clock, m.time_limit_s);
    const pyHolder = h("div"), sqlHolder = h("div");
    const prompt = h("textarea", { placeholder: "The prompt you would give an AI assistant for the Python task. The interviewer judges this." });
    main.append(h("div", { class: "bar" }, h("strong", {}, "Mock round"), clock),
      h("h2", {}, "Python: " + m.python.title), md(m.python.prompt), pyHolder,
      h("h2", {}, "SQL: " + m.sql.title), md(m.sql.prompt), h("pre", {}, m.sql.schema), sqlHolder,
      h("h2", {}, "Your prompt for the AI assistant"), prompt);
    const py = editor(pyHolder, "python", m.python.code), sql = editor(sqlHolder, "sql", m.sql.code);
    main.append(h("div", { class: "bar" }, h("button", { onclick: async (e) => {
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
        h("div", { class: "bar" }, h("button", { onclick: async (ev) => {
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
  main.replaceChildren();
  try { await view(); } catch (e) { main.append(h("pre", { class: "bad" }, String(e))); }
}

function route() {
  const [, name, id] = location.hash.split("/");
  if (name === "step") render(() => stepView(id));
  else if (name === "ex") render(() => exView(id));
  else if (name === "cards") render(cardsView);
  else if (name === "mock") render(mockView);
  else render(journeyView);
}

window.addEventListener("hashchange", route);
route();

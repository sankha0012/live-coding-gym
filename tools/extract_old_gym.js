// One-off: export the content constants of the old single-file gym to JSON.
// Run: node tools/extract_old_gym.js live-coding-gym.html tools/old_gym.json
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const at = (n) => html.indexOf("const " + n + " ");
const code = html.slice(at("SCHEMA"), at("VIEWS")).replace(/const runnable[\s\S]*?\n\}\n/, "const runnable = () => true;\n");
const out = new Function(code + "\nreturn {SCHEMA, DRILLS, TRACKS, LESSONS, CARDS, MOCKS, RUBRIC, STEPS};")();
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.log(Object.keys(out).map((k) => `${k}: ${Array.isArray(out[k]) ? out[k].length : typeof out[k]}`).join("\n"));

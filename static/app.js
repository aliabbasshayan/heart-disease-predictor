const form = document.getElementById("form");
const result = document.getElementById("result");
const els = {
  label: document.getElementById("result-label"),
  value: document.getElementById("result-value"),
  text: document.getElementById("result-text"),
  fill: document.getElementById("meter-fill"),
  submit: document.getElementById("submit"),
};

function clearErrors() {
  form.querySelectorAll(".field").forEach(f => {
    f.classList.remove("invalid");
    f.querySelector(".error").textContent = "";
  });
}

function showErrors(errors) {
  let first = null;
  for (const [name, msg] of Object.entries(errors)) {
    const field = form.querySelector(`.field[data-name="${name}"]`);
    if (!field) continue;
    field.classList.add("invalid");
    field.querySelector(".error").textContent = msg;
    first = first || field.querySelector("input, select");
  }
  if (first) first.focus();
}

function resetResult() {
  result.className = "panel result idle";
  els.label.textContent = "Result";
  els.value.textContent = "—";
  els.text.textContent = "Fill in the form and choose “Check risk”.";
  els.fill.style.width = "0";
}

function showResult(data) {
  const pct = Math.round(data.probability * 100);
  const positive = data.prediction === 1;
  result.className = "panel result run " + (positive ? "positive" : "negative");
  els.label.textContent = "Estimated probability of heart disease";
  els.value.textContent = pct + "%";
  els.text.textContent = positive
    ? "The model predicts heart disease is likely. Share these values with a doctor."
    : "The model predicts heart disease is unlikely based on these values.";
  els.fill.style.width = pct + "%";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearErrors();
  const payload = Object.fromEntries(new FormData(form).entries());
  els.submit.disabled = true;
  els.submit.textContent = "Checking…";
  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) { showErrors(data.errors || {}); return; }
    result.classList.remove("run");
    void result.offsetWidth; // restart the trace animation
    showResult(data);
  } catch {
    els.text.textContent = "Could not reach the server. Check that the app is running and try again.";
  } finally {
    els.submit.disabled = false;
    els.submit.textContent = "Check risk";
  }
});

document.getElementById("example").addEventListener("click", () => {
  clearErrors();
  form.querySelectorAll("input, select").forEach(el => { el.value = el.dataset.example; });
});

form.addEventListener("reset", () => { clearErrors(); resetResult(); });

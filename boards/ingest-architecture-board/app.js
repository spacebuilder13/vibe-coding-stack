import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

const diagramCanvas = document.getElementById("diagramCanvas");
const mermaidEl = document.getElementById("mermaid");
const blueprintEl = document.getElementById("blueprint");

let zoom = 1;

function setZoom(next) {
  zoom = Math.max(0.5, Math.min(2, next));
  diagramCanvas.style.transform = `scale(${zoom})`;
}

document.getElementById("zoomIn").addEventListener("click", () => setZoom(zoom + 0.1));
document.getElementById("zoomOut").addEventListener("click", () => setZoom(zoom - 0.1));
document.getElementById("resetZoom").addEventListener("click", () => setZoom(1));

document.getElementById("newIssueLink").href =
  "https://github.com/spacebuilder13/ingest-architecture-board/issues/new?title=Iteration%20feedback%3A%20ingest%20v3&body=What%20did%20you%20notice%3F%0A%0AWhat%20should%20change%3F%0A%0APriority%20%28P0%2FP1%2FP2%29%3A%20";

async function loadFiles() {
  const [diagramRes, blueprintRes] = await Promise.all([
    fetch("./data/ingest-v3-architecture.mmd"),
    fetch("./data/ingest-v3-agentic-blueprint.md"),
  ]);
  const diagramText = await diagramRes.text();
  const blueprintText = await blueprintRes.text();
  return { diagramText, blueprintText };
}

function mountGiscus() {
  const comments = document.getElementById("comments");
  comments.innerHTML = "";

  const script = document.createElement("script");
  script.src = "https://giscus.app/client.js";
  script.async = true;
  script.crossOrigin = "anonymous";
  script.setAttribute("data-repo", "spacebuilder13/ingest-architecture-board");
  script.setAttribute("data-repo-id", "R_kgDOSMxa9Q");
  script.setAttribute("data-category", "General");
  script.setAttribute("data-category-id", "DIC_kwDOSMxa9c4C7tVg");
  script.setAttribute("data-mapping", "pathname");
  script.setAttribute("data-strict", "0");
  script.setAttribute("data-reactions-enabled", "1");
  script.setAttribute("data-emit-metadata", "0");
  script.setAttribute("data-input-position", "top");
  script.setAttribute("data-theme", "dark_dimmed");
  script.setAttribute("data-lang", "en");
  comments.appendChild(script);
}

async function boot() {
  try {
    const { diagramText, blueprintText } = await loadFiles();
    mermaid.initialize({ startOnLoad: false, theme: "dark" });
    mermaidEl.textContent = diagramText;
    await mermaid.run({ querySelector: ".mermaid" });
    blueprintEl.innerHTML = marked.parse(blueprintText);
    mountGiscus();
  } catch (err) {
    mermaidEl.textContent = `Failed to load board assets: ${err.message}`;
  }
}

boot();

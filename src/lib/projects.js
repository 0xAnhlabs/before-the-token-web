import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const JSON_PATH = path.resolve(__dirname, "../../data/projects.json");

export function loadProjects() {
  if (!fs.existsSync(JSON_PATH)) return [];
  const raw = JSON.parse(fs.readFileSync(JSON_PATH, "utf-8"));
  return raw.projects || [];
}

export function getProject(slug) {
  return loadProjects().find((p) => p.project_row.slug === slug) || null;
}

// Human-readable category labels for slug-style values from DB.
const CATEGORY_LABELS = {
  "perpetual-futures-dex": "Perpetual Futures DEX",
};

export function displayCategory(raw) {
  return CATEGORY_LABELS[raw] || raw;
}

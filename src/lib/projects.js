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

// Load Pulse entries (compiled from vault markdown at build). Returns [] if file absent.
const PULSE_PATH = path.resolve(__dirname, "../../data/pulse.json");
export function loadPulse() {
  if (!fs.existsSync(PULSE_PATH)) return [];
  try {
    const raw = JSON.parse(fs.readFileSync(PULSE_PATH, "utf-8"));
    return raw.pulse || raw.projects || [];
  } catch (e) {
    return [];
  }
}

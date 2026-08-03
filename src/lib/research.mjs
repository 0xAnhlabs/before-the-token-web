import research from "../../data/research.js";

export function loadResearch(publishedOnly = false) {
  const items = Array.isArray(research) ? research : [];
  if (publishedOnly) {
    return items.filter((item) => item.status === "published");
  }
  return items;
}

export function findResearch(slug) {
  if (!slug) return null;
  const key = slug.toLowerCase();
  const items = Array.isArray(research) ? research : [];
  return items.find((item) => (item.slug || "").toLowerCase() === key) || null;
}

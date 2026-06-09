import { writable, derived } from "svelte/store";

function createUserId() {
  const stored = localStorage.getItem("dream_user_id");
  const id = stored || "user_" + Math.random().toString(36).slice(2, 10);
  if (!stored) localStorage.setItem("dream_user_id", id);
  return writable(id);
}

export const userId = createUserId();

export const currentPage = writable("home");
export const selectedEmotion = writable(null);

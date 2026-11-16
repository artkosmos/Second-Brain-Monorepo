import type { Note, NoteMutate } from "@/shared/types/notes";
import { request } from "@/services/api";

export const listNotes = () => request<Note[]>("/notes");

export const createNote = (note: NoteMutate) =>
  request<Note>("/notes", { method: "POST", body: JSON.stringify(note) });

export const updateNote = (id: number, note: NoteMutate) =>
  request<Note>(`/notes/${id}`, { method: "PUT", body: JSON.stringify(note) });

export const deleteNote = (id: number) => request<void>(`/notes/${id}`, { method: "DELETE" });

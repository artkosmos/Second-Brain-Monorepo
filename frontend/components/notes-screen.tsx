"use client";

import { useEffect, useMemo, useState } from "react";
import { NoteEditor } from "@/components/note-editor";
import { NoteList } from "@/components/note-list";
import { Sidebar } from "@/components/sidebar";
import { reportRequestError } from "@/external/errors";
import { createNote, deleteNote, listNotes, updateNote } from "@/services/notes";
import { type Note, type NoteMutate } from "@/shared/types/notes";

export function NotesScreen() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [draft, setDraft] = useState<NoteMutate | null>(null);
  const [query, setQuery] = useState("");
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [tagDraft, setTagDraft] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const getNotesList = () =>
    listNotes()
      .then((notes) => {
        setNotes(notes);
      })
      .catch((error: unknown) => {
        reportRequestError(error, "Failed to fetch notes");
      })
      .finally(() => {
        setIsLoading(false);
      });

  const startDraft = () => {
    setDraft((current) => current ?? { title: "", content: "", tags: [] });
    setSelectedId(null);
    setTagDraft("");
    setError(null);
    setQuery("");
    setActiveTag(null);
  };

  const createSelectedNote = async (note: NoteMutate) => {
    setIsLoading(true);
    try {
      const created = await createNote(note);
      await getNotesList();
      setDraft(null);
      setSelectedId(created.id);
    } catch (error: unknown) {
      reportRequestError(error, "Failed to create note");
      setIsLoading(false);
    }
  };

  const updateSelectedNote = async (note: NoteMutate) => {
    if (selectedId === null) return;
    setIsLoading(true);
    try {
      await updateNote(selectedId, note);
      await getNotesList();
    } catch (error: unknown) {
      reportRequestError(error, "Failed to update note");
      setIsLoading(false);
    }
  };

  const deleteSelected = async () => {
    if (selectedId === null && draft) {
      setDraft(null);
      setTagDraft("");
      setError(null);
      return;
    }
    if (selectedId === null) return;
    try {
      await deleteNote(selectedId);
      setIsLoading(true);
      await getNotesList();
      setSelectedId(notes[0]?.id ?? null);
      setTagDraft("");
      setError(null);
    } catch (error: unknown) {
      reportRequestError(error, "Failed to delete note");
    }
  };

  // Fetch notes list. Move to serverside later.
  useEffect(() => {
    void getNotesList();
  }, []);

  const editingDraft = selectedId === null && draft !== null;
  const selected = editingDraft ? draft : (notes.find((note) => note.id === selectedId) ?? null);

  const tags = useMemo(() => {
    const unique = new Set<string>();
    for (const note of notes) {
      for (const tag of note.tags ?? []) unique.add(tag);
    }
    for (const tag of draft?.tags ?? []) unique.add(tag);
    return [...unique];
  }, [notes, draft]);

  const matchesNote = (note: Note | NoteMutate) => {
    const noteTags = note.tags ?? [];
    const haystack = `${note.title} ${note.content} ${noteTags.join(" ")}`.toLowerCase();
    const matchesQuery = haystack.includes(query.trim().toLowerCase());
    const matchesTag = activeTag === null || noteTags.includes(activeTag);
    return matchesQuery && matchesTag;
  };

  const visibleNotes = notes.filter(matchesNote);
  const draftVisible = draft !== null && matchesNote(draft);

  const onChangeSelected = (patch: Partial<NoteMutate>) => {
    if (!selected) return;
    if (editingDraft && draft) {
      setDraft({ ...draft, ...patch });
      return;
    }
    setNotes((current) =>
      current.map((note) => (note.id === selectedId ? { ...note, ...patch } : note)),
    );
  };

  const saveSelected = () => {
    if (!selected) return;
    const title = selected.title.trim();
    const content = selected.content.trim();
    if (!title) {
      setError("Could not save: title cannot be empty");
      return;
    }
    if (!content) {
      setError("Could not save: content cannot be empty");
      return;
    }
    const noteTags = selected.tags ?? [];
    if (selectedId === null) {
      void createSelectedNote({
        title,
        content,
        tags: noteTags.map((tag) => tag.trim()).filter(Boolean),
      });
    } else {
      void updateSelectedNote({
        title,
        content,
        tags: noteTags.map((tag) => tag.trim()).filter(Boolean),
      });
    }
    setError(null);
  };

  const addTag = () => {
    if (!selected) return;
    const tag = tagDraft.trim();
    const noteTags = selected.tags ?? [];
    if (!tag || noteTags.includes(tag)) {
      setTagDraft("");
      return;
    }
    onChangeSelected({ tags: [...noteTags, tag] });
    setTagDraft("");
  };

  const selectDraft = () => {
    setSelectedId(null);
    setTagDraft("");
    setError(null);
  };

  const selectNote = (id: number) => {
    setSelectedId(id);
    setTagDraft("");
    setError(null);
  };

  return (
    <div className="flex h-full bg-paper text-ink">
      <Sidebar />
      <NoteList
        query={query}
        onQueryChange={setQuery}
        isLoading={isLoading}
        tags={tags}
        activeTag={activeTag}
        onToggleTag={(tag) => setActiveTag(activeTag === tag ? null : tag)}
        onNewNote={startDraft}
        hasNotes={notes.length > 0}
        notes={visibleNotes}
        draft={draft}
        draftVisible={draftVisible}
        editingDraft={editingDraft}
        selectedId={selectedId}
        onSelectDraft={selectDraft}
        onSelectNote={selectNote}
      />
      <NoteEditor
        isLoading={isLoading}
        note={selected}
        error={error}
        tagDraft={tagDraft}
        onTagDraftChange={setTagDraft}
        onChange={onChangeSelected}
        onAddTag={addTag}
        onDelete={() => void deleteSelected()}
        onSave={saveSelected}
        onNewNote={startDraft}
      />
    </div>
  );
}

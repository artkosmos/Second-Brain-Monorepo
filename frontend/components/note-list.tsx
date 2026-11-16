import { Button } from "@/components/Button/Button";
import { Spinner } from "@/components/spinner";
import { NoteListItem } from "@/components/note-list-item";
import type { Note, NoteMutate } from "@/shared/types/notes";

type NoteListProps = {
  query: string;
  onQueryChange: (query: string) => void;
  isLoading: boolean;
  tags: string[];
  activeTag: string | null;
  onToggleTag: (tag: string) => void;
  onNewNote: () => void;
  hasNotes: boolean;
  notes: Note[];
  draft: NoteMutate | null;
  draftVisible: boolean;
  editingDraft: boolean;
  selectedId: number | null;
  onSelectDraft: () => void;
  onSelectNote: (id: number) => void;
};

export function NoteList({
  query,
  onQueryChange,
  isLoading,
  tags,
  activeTag,
  onToggleTag,
  onNewNote,
  hasNotes,
  notes,
  draft,
  draftVisible,
  editingDraft,
  selectedId,
  onSelectDraft,
  onSelectNote,
}: NoteListProps) {
  return (
    <section className="flex w-95 shrink-0 flex-col border-r border-line">
      <div className="flex flex-col gap-3 border-b border-line p-4">
        <input
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Find a note"
          className="h-10 rounded-xl border border-line bg-sheet px-3 text-sm outline-none placeholder:text-faint focus:border-moss"
        />
        {isLoading ? (
          <div className="flex justify-center p-1">
            <Spinner label="Loading tags" />
          </div>
        ) : tags.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {tags.map((tag) => {
              const active = activeTag === tag;
              return (
                <button
                  key={tag}
                  type="button"
                  onClick={() => onToggleTag(tag)}
                  className={
                    active
                      ? "h-6 rounded-full border border-moss bg-moss px-2 text-[11px] font-medium text-sheet"
                      : "h-6 rounded-full border border-line-strong bg-recessed px-2 text-[11px] font-medium text-muted"
                  }
                >
                  {tag}
                </button>
              );
            })}
          </div>
        ) : null}
        <Button onClick={onNewNote}>New note</Button>
      </div>
      <div className="flex-1 overflow-y-auto p-3">
        {isLoading ? (
          <div className="flex justify-center p-2">
            <Spinner label="Loading notes" size="size-6" />
          </div>
        ) : !hasNotes && !draft ? (
          <p className="px-2 py-6 text-center text-sm text-muted">No notes yet</p>
        ) : !draftVisible && notes.length === 0 ? (
          <p className="px-2 py-6 text-sm text-muted">No notes match</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {draftVisible && draft && (
              <li key="draft">
                <NoteListItem
                  title={draft.title}
                  content={draft.content}
                  active={editingDraft}
                  onSelect={onSelectDraft}
                />
              </li>
            )}
            {notes.map((note) => (
              <li key={note.id}>
                <NoteListItem
                  title={note.title}
                  content={note.content}
                  tags={note.tags ?? []}
                  active={note.id === selectedId}
                  onSelect={() => onSelectNote(note.id)}
                />
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}

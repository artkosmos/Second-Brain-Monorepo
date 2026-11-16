import { Button } from "@/components/Button/Button";
import { Spinner } from "@/components/spinner";
import type { NoteMutate } from "@/shared/types/notes";

type NoteEditorProps = {
  isLoading: boolean;
  note: NoteMutate | null;
  error: string | null;
  tagDraft: string;
  onTagDraftChange: (value: string) => void;
  onChange: (patch: Partial<NoteMutate>) => void;
  onAddTag: () => void;
  onDelete: () => void;
  onSave: () => void;
  onNewNote: () => void;
};

export function NoteEditor({
  isLoading,
  note,
  error,
  tagDraft,
  onTagDraftChange,
  onChange,
  onAddTag,
  onDelete,
  onSave,
  onNewNote,
}: NoteEditorProps) {
  if (isLoading) {
    return (
      <main className="flex min-w-0 flex-1 flex-col">
        <div className="flex flex-1 items-center justify-center">
          <Spinner label="Loading note" size="size-6" />
        </div>
      </main>
    );
  }

  if (!note) {
    return (
      <main className="flex min-w-0 flex-1 flex-col">
        <div className="flex flex-1 flex-col items-center justify-center gap-4">
          <p className="text-sm text-muted">No notes yet</p>
          <Button onClick={onNewNote} className="px-4">
            New note
          </Button>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-w-0 flex-1 flex-col">
      {error && (
        <p className="mx-8 mt-6 rounded-xl border border-danger-line bg-danger-bg px-4 py-2 text-sm text-danger">
          {error}
        </p>
      )}
      <div className="mx-auto flex w-full max-w-195 flex-1 flex-col px-10 py-12">
        <input
          value={note.title}
          onChange={(event) => onChange({ title: event.target.value })}
          placeholder="Title"
          className="w-full bg-transparent font-serif text-[40px] leading-12 tracking-tight outline-none placeholder:text-faint"
        />
        <textarea
          value={note.content}
          onChange={(event) => onChange({ content: event.target.value })}
          placeholder="Start writing"
          className="mt-6 min-h-48 w-full flex-1 resize-none bg-transparent text-base leading-6.5 outline-none placeholder:text-faint"
        />
        <div className="mt-6 flex flex-wrap items-center gap-2">
          {(note.tags ?? []).map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() =>
                onChange({ tags: (note.tags ?? []).filter((item) => item !== tag) })
              }
              className="h-6 rounded-full border border-line-strong bg-recessed px-2 text-[11px] font-medium text-muted"
            >
              {tag}
            </button>
          ))}
          <input
            value={tagDraft}
            onChange={(event) => onTagDraftChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                onAddTag();
              }
            }}
            placeholder="add a tag"
            className="h-6 min-w-24 bg-transparent text-[13px] outline-none placeholder:text-faint"
          />
        </div>
      </div>
      <div className="flex justify-end gap-2 border-t border-line px-8 py-4">
        <button
          type="button"
          onClick={onDelete}
          className="h-9 rounded-lg border border-danger-line px-4 text-sm text-danger hover:bg-danger-bg"
        >
          Delete
        </button>
        <Button onClick={onSave} className="px-4">
          Save
        </Button>
      </div>
    </main>
  );
}

type NoteListItemProps = {
  title: string;
  content: string;
  tags?: string[];
  active: boolean;
  onSelect: () => void;
};

export function NoteListItem({ title, content, tags, active, onSelect }: NoteListItemProps) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={
        active
          ? "w-full rounded-xl border border-moss bg-recessed p-4 text-left"
          : "w-full rounded-xl border border-line bg-sheet p-4 text-left hover:bg-recessed"
      }
    >
      <h2 className="font-serif text-xl leading-7 font-medium">{title.trim() || "Untitled"}</h2>
      {content.trim() && (
        <p className="mt-1 line-clamp-2 text-[13px] leading-4.5 text-muted">{content}</p>
      )}
      {tags && tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {tags.slice(0, 2).map((tag) => (
            <span
              key={tag}
              className="inline-flex h-6 items-center rounded-full border border-line-strong bg-sheet px-2 text-[11px] font-medium text-muted"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </button>
  );
}

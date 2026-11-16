export type Note = {
  id: number;
  title: string;
  content: string;
  tags?: string[];
};

export type NoteMutate = {
  title: string;
  content: string;
  tags: string[];
};

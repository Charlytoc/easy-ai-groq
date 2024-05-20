import { Remarkable } from "remarkable";
//
export const markdownToHtml = (content: string) => {
  const md = new Remarkable();
  return md.render(content);
};

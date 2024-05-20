import { Toaster } from "react-hot-toast";
import { Chat } from "./components/Chat/Chat";

export default function Root() {
  return (
    <main>
      <Toaster />
      <Chat />
    </main>
  );
}

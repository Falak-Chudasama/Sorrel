import { useChat } from './hooks/useChat';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';

export default function App() {
	const { messages, isLoading, error, send, bottomRef } = useChat();

	return (
		<div className="flex flex-col h-screen w-full bg-zinc-950 text-zinc-100 overflow-hidden">
			<header className="flex-none bg-zinc-950/80 backdrop-blur-md border-b border-zinc-800 px-6 py-4 flex items-center justify-between z-10 sticky top-0">
				<div className="flex items-center gap-3">
					<div className="w-8 h-8 rounded-md bg-red-600 flex items-center justify-center font-bold text-white shadow-md shadow-red-900/30">
						S
					</div>
					<h1 className="text-lg font-semibold tracking-wide text-zinc-100">Sorrel</h1>
				</div>
				<div className="text-[11px] uppercase tracking-wider font-semibold text-zinc-400 border border-zinc-800 px-3 py-1.5 rounded-full bg-zinc-900">
					Academic Database
				</div>
			</header>

			{error && (
				<div className="bg-red-500/10 border-b border-red-500/20 text-red-400 px-4 py-3 text-sm text-center flex-none font-medium">
					{error}
				</div>
			)}

			<ChatWindow messages={messages} isLoading={isLoading} bottomRef={bottomRef} />

			<InputBar onSend={send} isLoading={isLoading} />
		</div>
	);
}
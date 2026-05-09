import MessageBubble from './MessageBubble';

export default function ChatWindow({ messages, isLoading, bottomRef }) {
    return (
        <div className="flex-1 overflow-y-auto p-4 md:p-8 scroll-smooth">
            <div className="max-w-4xl mx-auto w-full">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-zinc-500 mt-[15vh]">
                        <div className="w-16 h-16 bg-zinc-900 rounded-2xl flex items-center justify-center mb-6 border border-zinc-800 shadow-sm">
                            <span className="text-red-500 font-bold text-2xl">S</span>
                        </div>
                        <h2 className="text-xl font-medium text-zinc-300 mb-3">Sorrel</h2>
                        <p className="text-[15px] text-center max-w-sm leading-relaxed">
                            Your academic policy assistant. Ask me about exams, deadlines, and institutional regulations.
                        </p>
                    </div>
                ) : (
                    messages.map((msg, i) => (
                        <MessageBubble key={i} message={msg} />
                    ))
                )}

                {isLoading && (
                    <div className="flex w-full justify-start mb-6">
                        <div className="bg-zinc-800/80 border border-zinc-700/50 rounded-2xl rounded-bl-sm px-5 py-5 flex items-center gap-1.5 shadow-sm">
                            <div className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce"></div>
                            <div className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: '0.15s' }}></div>
                            <div className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" style={{ animationDelay: '0.3s' }}></div>
                        </div>
                    </div>
                )}
                <div ref={bottomRef} className="h-2" />
            </div>
        </div>
    );
}
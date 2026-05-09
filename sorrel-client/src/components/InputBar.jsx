import { useState } from 'react';

export default function InputBar({ onSend, isLoading }) {
    const [input, setInput] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <div className="w-full bg-zinc-950 border-t border-zinc-800 p-4 shrink-0">
            <div className="max-w-4xl mx-auto">
                <form onSubmit={handleSubmit} className="relative flex items-center shadow-lg rounded-xl">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about exam rules, policies, or deadlines..."
                        disabled={isLoading}
                        className="w-full bg-zinc-900 border border-zinc-700 text-zinc-100 rounded-xl pl-5 pr-14 py-4 text-[15px] focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 transition-colors disabled:opacity-50 placeholder:text-zinc-500"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2.5 p-2 bg-red-600 text-white rounded-lg hover:bg-red-500 disabled:bg-zinc-800 disabled:text-zinc-600 transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                            <path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" />
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    );
}
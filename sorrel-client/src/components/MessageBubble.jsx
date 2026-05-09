import SourceBadge from './SourceBadge';

export default function MessageBubble({ message }) {
    const isUser = message.role === 'user';

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
            <div
                className={`max-w-[85%] md:max-w-[75%] rounded-2xl px-5 py-4 shadow-sm ${isUser
                        ? 'bg-red-600 text-white rounded-br-sm'
                        : 'bg-zinc-800/80 text-zinc-100 rounded-bl-sm border border-zinc-700/50'
                    }`}
            >
                <div className="whitespace-pre-wrap leading-relaxed text-[15px]">{message.content}</div>

                {!isUser && message.sources?.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-zinc-700/50 flex flex-wrap">
                        {message.sources.map((src, i) => (
                            <SourceBadge key={i} source={src} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
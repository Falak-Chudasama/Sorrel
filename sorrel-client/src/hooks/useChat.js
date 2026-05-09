import { useState, useEffect, useRef } from 'react';
import { sendMessage, getNewSession } from '../api/chatApi';

export function useChat() {
    const [sessionId, setSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const bottomRef = useRef(null);

    useEffect(() => {
        const initSession = async () => {
            try {
                const { session_id } = await getNewSession();
                setSessionId(session_id);
            } catch (err) {
                setError('Failed to connect to the server.');
            }
        };
        initSession();
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const send = async (text) => {
        if (!text.trim() || isLoading || !sessionId) return;

        const userMessage = { role: 'user', content: text, sources: [] };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const data = await sendMessage(sessionId, text);
            const assistantMessage = {
                role: 'assistant',
                content: data.response,
                sources: data.sources || []
            };
            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            setError('Something went wrong. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return { messages, isLoading, error, send, bottomRef };
}
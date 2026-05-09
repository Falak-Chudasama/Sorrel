import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:4000';

export async function getNewSession() {
    const res = await axios.get(`${API_BASE}/api/session/new`);
    return res.data;
}

export async function sendMessage(session_id, message) {
    const res = await axios.post(`${API_BASE}/api/chat`, { session_id, message });
    return res.data;
}
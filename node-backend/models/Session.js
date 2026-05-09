const mongoose = require('mongoose');

const SourceSchema = new mongoose.Schema({
    source_file: String,
    section_heading: String,
    page_number: String,
    relevance_score: Number
}, { _id: false });

const MessageSchema = new mongoose.Schema({
    role: { type: String, enum: ['user', 'assistant'], required: true },
    content: { type: String, required: true },
    timestamp: { type: Date, default: Date.now },
    sources: [SourceSchema]
}, { _id: false });

const SessionSchema = new mongoose.Schema({
    session_id: { type: String, required: true, unique: true, index: true },
    created_at: { type: Date, default: Date.now },
    updated_at: { type: Date, default: Date.now },
    messages: [MessageSchema]
});

module.exports = mongoose.model('Session', SessionSchema);
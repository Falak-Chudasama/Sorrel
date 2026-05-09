const express = require('express');
const router = express.Router();
const axios = require('axios');
const Session = require('../models/Session');

const PYTHON_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

router.post('/', async (req, res, next) => {
    try {
        const { session_id, message } = req.body;

        if (!session_id || !message?.trim()) {
            return res.status(400).json({ error: 'session_id and message are required.' });
        }

        const pythonResponse = await axios.post(`${PYTHON_URL}/api/chat`, {
            session_id,
            message: message.trim()
        });

        const { response, sources } = pythonResponse.data;

        await Session.findOneAndUpdate(
            { session_id },
            {
                $set: { updated_at: new Date() },
                $push: {
                    messages: {
                        $each: [
                            { role: 'user', content: message.trim(), timestamp: new Date(), sources: [] },
                            { role: 'assistant', content: response, timestamp: new Date(), sources }
                        ]
                    }
                }
            },
            { upsert: true, new: true }
        );

        res.json({ response, sources, session_id });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
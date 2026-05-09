const express = require('express');
const router = express.Router();
const Session = require('../models/Session');
const { v4: uuidv4 } = require('uuid');

router.get('/new', (req, res) => {
    const session_id = uuidv4();
    res.json({ session_id });
});

router.get('/:session_id', async (req, res, next) => {
    try {
        const session = await Session.findOne({ session_id: req.params.session_id });
        if (!session) return res.json({ messages: [] });
        res.json({ messages: session.messages });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
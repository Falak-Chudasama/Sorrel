const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
require('dotenv').config();
const connectDB = require('./config/db');
const chatRoutes = require('./routes/chat');
const sessionRoutes = require('./routes/session');
const errorHandler = require('./middleware/errorHandler');

const app = express();
const PORT = process.env.PORT || 4000;

connectDB();

app.use(cors({ origin: '*' }));
app.use(express.json());
app.use(morgan('dev'));

app.use('/api/chat', chatRoutes);
app.use('/api/session', sessionRoutes);
app.use(errorHandler);

app.listen(PORT, () => console.log(`Express server running on port ${PORT}`));
const express = require('express');
const cors = require('cors');
const app = express();

// Enable CORS for all routes
app.use(cors());

// Body parser middleware to handle JSON request bodies
app.use(express.json());

// Your chat endpoint
app.post('/chat', (req, res) => {
    const question = req.body.question;
    
    // Handle the request here, return an appropriate response
    res.json({ answer: `You asked: ${question}` });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

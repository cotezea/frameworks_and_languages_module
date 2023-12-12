const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const itemsRoutes = require('./routes/itemsRoutes');

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('tiny'));

app.use('/api/items', itemsRoutes);

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
const express = require('express');
const { getAllItems, addItem } = require('../controllers/itemsController');

const router = express.Router();

router.get('/', getAllItems);
router.post('/', addItem);

module.exports = router;
exports.getAllItems = (req, res) => {
    // Logic to get all items
};

exports.addItem = (req, res) => {
    // Logic to add an item
};
// app.js

const express = require('express');
const itemsRoutes = require('./routes/itemsRoutes');

const app = express();

app.use(express.json()); // Middleware to parse JSON bodies

// Use itemsRoutes for the '/api/items' path
app.use('/api/items', itemsRoutes);

// ... rest of your Express app setup ...


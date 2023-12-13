// Importing Express and the controller functions
const express = require('express');
const { getAllItems, addItem } = require('../controllers/itemsController');
const router = express.Router();
// Define routes
router.get('/', getAllItems);
router.post('/', addItem);

module.exports = router;


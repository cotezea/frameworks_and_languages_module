let items = []; // Mock database for storing items
exports.getAllItems = (req, res) => {
    res.status(200).json(items);
};
exports.addItem = (req, res) => {
    const newItem = req.body; // Assuming the item's data is sent in the request body
    items.push(newItem); // Add the new item to the array (mock database)
    res.status(201).json({ message: 'Item added', item: newItem });
};


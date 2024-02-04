// Requiring module
const express = require('express');
const mongoose = require('mongoose');
 
// Creating express object
const app = express();

app.use(express.json()); 
// Handling GET request
app.get('/', (req, res) => { 
    res.send('A simple Node App is '
        + 'running on this server') 
    res.end() 
}) 
 
// Port Number
const PORT = process.env.PORT ||5000;
 
// Server Setup
app.listen(PORT,console.log(
  `Server started on port ${PORT}`));
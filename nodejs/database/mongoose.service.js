const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/rinha_db');

mongoose.connection.on('connected', () => {
    console.log('Connected to MongoDB');
});

mongoose.connection.on('error', (err) => {
    console.error('Error connecting to MongoDB:', err);
});

mongoose.connection.on('disconnected', () => {
    console.log('Disconnected from MongoDB');
});

process.on('SIGINT', () => {
  mongoose.disconnect(() => {
    console.log('Disconnected from MongoDB due to application termination');
    process.exit(0);
  });
});

exports.mongoose = mongoose;
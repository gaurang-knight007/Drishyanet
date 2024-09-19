const express = require('express');
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');
const path = require('path');
const multer = require('multer');

const app = express();
const port = 3000;

// Multer configuration for handling file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage });

const url = 'mongodb://localhost:27017';
const dbName = 'userdb';
const dbName2 = 'userdb2';

let db;
let db2;

MongoClient.connect(url, { useNewUrlParser: true, useUnifiedTopology: true })
  .then((client) => {
    console.log('Connected to MongoDB');

    db = client.db(dbName);
    db2 = client.db(dbName2);

    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });
  })
  .catch((err) => {
    console.error('Error connecting to MongoDB:', err);
    process.exit(1);
  });

app.use(express.static(path.join(__dirname, 'public')));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

app.use(upload.single('image'));

// routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/signup', async (req, res) => {
  const { name, email, password } = req.body;

  if (!db)
  {
    console.error('MongoDB connection not established');
    return res.status(500).send('Internal Server Error');
  }

  const existingUser = await db.collection('users').findOne({ email });
  if (existingUser)
  {
    console.error('Email already exists');
    return res.status(409).send('Email already exists');
  }

  db.collection('users').insertOne({ name, email, password }, (err, result) => {
    if (err)
    {
      console.error('Error inserting user into MongoDB:', err);
      return res.status(500).send('Internal Server Error');
    }

    console.log('User entered');
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
    console.log('redirected');
  });
});

app.post('/signin', async (req, res) => {
  const { email, password } = req.body;

  if (!db)
  {
    console.error('MongoDB connection not established');
    return res.status(500).send('Internal Server Error');
  }

  console.log('Received login request:', email, password);

  const user = await db.collection('users').findOne({ email, password });

  if (user)
  {
    console.log('Redirecting to attendance.html');
    res.sendFile(path.join(__dirname, 'public', 'attendance.html'));
  }
  else
  {
    console.error('Invalid email or password');
    res.status(401).send('Invalid email or password');
  }
});

app.post('/proceed', (req, res) => {
  console.log('Received proceed request');
  res.sendFile(path.join(__dirname, 'public', 'index3.html'));
  console.log('redirected');
});

app.post('/proceed1', (req, res) => {
  console.log('Received proceed request');
  res.sendFile(path.join(__dirname, 'public', 'index4.html'));
  console.log('redirected');
});

app.post('/api/register', async (req, res) => {
  const { name, rollNo, phone } = req.body;
  if (!db2)
  {
    console.error('Second MongoDB connection not established');
    return res.status(500).send('Internal Server Error');
  }

  try
  {
    const image = req.file ? req.file.buffer : null;
    await db2.collection('users').insertOne({ name, rollNo, phone, image });
    console.log('User data inserted into userdb2');
    res.json({ success: true });
  }
  catch (error)
  {
    console.error('Error inserting user into userdb2:', error);
    res.status(500).json({ success: false, error: 'Internal Server Error' });
  }
});

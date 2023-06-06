const express = require('express');

const app = express();
const cors = require('cors');

const router = require('./router');
const {port} = require('./config');
app.use(express.json());
app.use(cors());

app.use('/api/v1/docs/summary', router);
app.listen(port, () => console.log(`Server started on port ${port}`));

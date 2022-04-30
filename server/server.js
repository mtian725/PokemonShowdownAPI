
// Following model in MongoDB Express REST API example
require("dotenv").config({ path: "../config.env" })
const express = require("express");
const cors = require("cors");
const dbo = require("./db/connection");

const PORT = process.env.PORT || 3000;

const app = express();
app.use(cors());
app.use(express.json());
app.use(require("./routes/record"));

app.use(function (err, _req, res) {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

dbo.connectToServer(function (err) {
    if (err) {
        console.error(err);
        process.exit();
    }

    app.listen(PORT, () => {
        console.log(`Server is running on port: ${PORT}`);
    });
});
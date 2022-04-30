
const express = require("express");
const recordRoutes = express.Router();
const db = require("../db/connection");

// temporary, replace this later
recordRoutes.route("/data/:tagID").get(async function(req, res) {
    const dbConnect = db.getDb();

    dbConnect
        .collection("2022-03/gen8uu-0")
        .find({})
        .toArray(function (err, result) {
            if (err) {
                res.status(400).send("Error fetching listings!");
            } else {
                res.json(result)
            }
        });
});

recordRoutes.route("/*").get(async function(req, res) {
    const dbConnect = db.getDb();
    const query = req.path.substring(1)
    
    // To santize the query to some degree
    const regex = /^\d{4}-\d{2}(\/.+)+$/;

    if (regex.test(query)) {
        dbConnect
        .collection(query)
        .find({})
        .toArray(function (err, result) {
            if (err) {
                res.status(400).send("Error fetching listings!");
            } else {
                res.json(result)
            }
        });
    } else {
        res.status(400).send("Invalid Request!");
    }
});


module.exports = recordRoutes;
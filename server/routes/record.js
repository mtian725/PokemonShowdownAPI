
const express = require("express");
const recordRoutes = express.Router();
const db = require("../db/connection");

/**
 * TODO:
 * Determine a better way to route things
 * Make sure cleaning for dates also takes into account the edge cases like
 * - 2022-06-DLC1 or 2022-11-H1
 * 
 * How MUCH data do I want up there?
 * MongoDB Atlas only has 512 MB of free data
 */

recordRoutes.route('/:date/:tier').get(async function(req, res) {
    const dbConnect = db.getDb();

    dbConnect
        .collection(`${req.params.date}/${req.params.tier}`)
        .find({})
        .toArray(function (err, result) {
            if (err) {
                res.status(400).send("Error fetching listings!");
            } else {
                res.json(result)
            }
        });
})

recordRoutes.route("/*").get(async function(req, res) {
    const dbConnect = db.getDb();

    res.status(404).send(`Invalid request for query ${req.path}`)
})

module.exports = recordRoutes;
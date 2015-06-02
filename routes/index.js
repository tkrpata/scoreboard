var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  json = { 'delta' : global.delta };
  global.delta = 0;
  res.json(json);
});

module.exports = router;

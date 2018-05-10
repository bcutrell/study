#! /usr/bin/env node

console.log('This script populates some stocks and stockinstances. Specified database as argument - e.g.: populatedb mongodb://your_username:your_password@your_dabase_url');

// Get arguments passed on command line
var userArgs = process.argv.slice(2);
if (!userArgs[0].startsWith('mongodb://')) {
  console.log('ERROR: You need to specify a valid mongodb URL as the first argument');
  return
}

var async = require('async')
var Stock = require('./models/stock')
var StockInstance = require('./models/stockinstance')

var mongoose = require('mongoose');
var mongoDB = userArgs[0];
mongoose.connect(mongoDB);
mongoose.Promise = global.Promise;
var db = mongoose.connection;
mongoose.connection.on('error', console.error.bind(console, 'MongoDB connection error:'));

var stocks = [];
var stockinstances = [];


function stockCreate(symbol, sector, name, cb) {
  stockdetail = {symbol: symbol, sector: sector, name: name }
  var stock = new Stock(stockdetail);

  stock.save(function (err) {
    if (err) {
      cb(err, null)
      return
    }

    console.log('New Stock: ' + stock);
    stocks.push(stock)
    cb(null, stock)
  });
}

function stockInstanceCreate(stock, close_price, date, cb) {
  stockinstancedetail = { stock: stock, close_price: close_price, date: date }
  var stockinstance = new StockInstance(stockinstancedetail);

  stockinstance.save(function (err) {
    if (err) {
      cb(err, null)
      return
    }

    console.log('New Stock Instance: ' + stockinstance);
    stockinstances.push(stockinstances)
    cb(null, stockinstances)
  });
}


function createStocks(cb) {
  async.parallel([
    function(callback) {
      stockCreate('AAPL', 'Technology', 'Apple Inc.', callback);
    }
  ], cb)
}

function createStockInstances(cb) {
  async.parallel([
    function(callback) {
      stockInstanceCreate(stocks[0], 100.0, '2018-05-04', callback);
    }
  ], cb)
}


async.series([
  createStocks,
  createStockInstances
],
// Optional callback
function(err, results) {
  if (err) {
    console.log('FINAL ERR: '+err);
  }
  else {
    console.log('StockInstances: '+stockinstances);
  }

  // All done, disconnect from database
  mongoose.connection.close();
});


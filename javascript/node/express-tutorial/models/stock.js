var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var StockSchema = new Schema(
  {
    symbol: { type: String, required: true, max: 10 },
    sector: { type: String, max: 100 },
    name:   { type: String, max: 100 },
    date_of_birth: {type: Date},
    date_of_death: {type: Date},
  }
);

StockSchema
.virtual('url')
.get(function () {
  return '/quote/' + this.symbol;
});

module.exports = mongoose.model('Stock', StockSchema);


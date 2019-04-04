var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var StockInstanceSchema = new Schema(
  {
    stock: { type: Schema.ObjectId, ref: 'Stock', required: true },
    close_price: { type: Number, required: true },
    date:   { type: Date }
  }
);

module.exports = mongoose.model('StockInstance', StockInstanceSchema);



var config = require('./config');

// curl ""
// start_date
// end_date
const https = require('https');

let params = '?api_key=' + config.quandl.api_key +
  '&start_date=2017-01-01&end_date=2018-01-01'
let url = 'https://www.quandl.com/api/v3/datasets/WIKI/FB/data.json?' + params

https.get(url, (resp) => {
  let data = '';

  resp.on('data', (chunk) => {
    data += chunk
  })

  resp.on('end', () => {
    console.log(JSON.parse(data));
  });

}).on('error', (err) => {
  console.log('Error: ' + err.message);
});


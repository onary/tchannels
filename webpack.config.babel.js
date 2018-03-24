const path = require('path');

module.exports = {
  entry: './frontend/index.js',
  output: {
    path: path.resolve('static'),
    filename: 'app.js'
  },
  mode: 'development',
  module: {
    rules: [
      { test: /\.css$/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader" }
        ]
      },
      {
        test: /\.js|.jsx?$/,
        exclude: /node_modules/,
        use: "babel-loader"
      }
    ]
  }
}


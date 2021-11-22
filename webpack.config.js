const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    entry: './taskproductivity/jsx/main.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'taskproductivity', 'static', "taskproductivity", "js"),
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-react']
                    }
                }
            }
        ]
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
    }
};
const webpack = require('webpack');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config();

module.exports = {
    mode: 'development',  // или 'production'
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env.HOST_USA': JSON.stringify(process.env.HOST_USA),
            'process.env.PORT_USA': JSON.stringify(process.env.PORT_USA),
            'process.env.HOST_DE': JSON.stringify(process.env.HOST_DE),
            'process.env.PORT_DE': JSON.stringify(process.env.PORT_DE),
            'process.env.HOST_UK': JSON.stringify(process.env.HOST_UK),
            'process.env.PORT_UK': JSON.stringify(process.env.PORT_UK),
            'process.env.HOST_FR': JSON.stringify(process.env.HOST_FR),
            'process.env.PORT_FR': JSON.stringify(process.env.PORT_FR),
            'process.env.LOGIN_PROXY': JSON.stringify(process.env.LOGIN_PROXY),
            'process.env.PASS_PROXY': JSON.stringify(process.env.PASS_PROXY)
        })
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
            },
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx', '.json']
    }
};

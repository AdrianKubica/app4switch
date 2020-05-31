module.exports = {
    configureWebpack: {
        devtool: 'source-map'
    },
    publicPath: '/',
    devServer: {
        proxy: 'http://localhost:8000'
    },
    chainWebpack: config => {
        config.performance
            .hints(false)
    }
};
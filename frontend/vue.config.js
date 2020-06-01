module.exports = {
  configureWebpack: {
    devtool: "source-map"
  },
  publicPath: "/",
  devServer: {
    proxy: "http://192.168.99.110:9000"
  },
  chainWebpack: config => {
    config.performance.hints(false);
  }
};

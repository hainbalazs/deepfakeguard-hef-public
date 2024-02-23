const { defineConfig } = require('@vue/cli-service');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = defineConfig({
  publicPath: process.env.NODE_ENV === 'production'
    ? '/frontend/'  // Set the correct path for your production assets
    : '/',
  transpileDependencies: true,
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'Human Evaluation Framework'; 
      return args;
    });
  }
});

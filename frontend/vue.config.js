const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js', // путь к основному файлу Vue
      template: 'public/templates/index.html', // путь к HTML файлу в public/templates
      filename: 'index.html', // имя выходного файла
      title: 'Home Page', // заголовок страницы
    },
  },
  chainWebpack: config => {
    config.plugin('html-index').tap(args => {
      args[0].template = path.resolve(__dirname, 'public/templates/index.html');
      return args;
    });
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    watchFiles: ['src/**/*', 'public/**/*'],
  },
});
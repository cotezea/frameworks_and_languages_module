const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: true, // Enable HTTPS
    // Other devServer configurations can go here
  },
});

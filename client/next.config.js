const withCss = require('@zeit/next-css');

module.exports = withCss({
  exportPathMap: () => ({
    '/': { page: '/' },
  }),
});

const hooks = require('hooks');

hooks.beforeEach((transaction) => {
  // Historically, the API is only available to browsers to prevent bots
  // logging chats, even if they ignore robots.txt
  transaction.request.headers['User-Agent'] = 'User-Agent: Mozilla/5.0 (Android; Mobile; rv:13.0) Gecko/13.0 Firefox/13.0';

  transaction.request.headers.Accept = 'application/json';
});

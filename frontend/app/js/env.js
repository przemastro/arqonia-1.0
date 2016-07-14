
//DEV Environment
(function (window) {
  window.__env = window.__env || {};

  // API url
  window.__env.apiUrl = 'http://localhost:5001';
  window.__env.apiUrlService = 'http://localhost\\:5001';

  window.__env.enableDebug = true;
}(this));


//UAT Environment
/*
(function (window) {
  window.__env = window.__env || {};

  // API url
  window.__env.apiUrl = 'http://10.61.3.121:5000';
  window.__env.apiUrlService = 'http://10.61.3.121\\:5000';

  // Base url
  window.__env.baseUrl = '/';

  window.__env.enableDebug = true;
}(this));
*/

//PROD Environment
/*
(function (window) {
  window.__env = window.__env || {};

  // API url
  window.__env.apiUrl = 'http://213.156.98.92:5001';
  window.__env.apiUrlService = 'http://213.156.98.92\\:5001';

  // Base url
  window.__env.baseUrl = '/';

  window.__env.enableDebug = true;
}(this));
*/
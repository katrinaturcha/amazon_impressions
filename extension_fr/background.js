// Определение конфигурации прокси
var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: process.env.HOST_FR,
        port: parseInt(process.env.PORT_FR)
      },
      bypassList: ["localhost"]
    }
};

// Установка настроек прокси
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {
    console.log('Proxy settings updated.');
});

// Функция для авторизации на прокси
function callbackFn(details) {
    return {
        authCredentials: {
            username: process.env.LOGIN_PROXY,  // Использование переменной окружения
            password: process.env.PASS_PROXY   // Использование переменной окружения
        }
    };
}

// Добавление слушателя для обработки требований прокси-аутентификации
chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);

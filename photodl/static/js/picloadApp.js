var picloadApp = angular.module("picloadApp", []);

picloadApp.config(function($locationProvider, $routeProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider
        .when('/',  {
            templateUrl: '../../templates/index.html',
            controller: 'MainController'
        })
        .when('/user', {
            templateUrl: '../../templates/user.html',
            controller: 'UserController'
        })
        .when('/media', {
            templateUrl: '../../templates/media.html',
            controller: 'MediaController'
        })
        .otherwise({
            redirectTo: '/'
        })
});

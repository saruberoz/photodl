
picload.controller('MainController', function($scope) {
    $scope.data = 'main controller'
});

picload.controller('UserController', function($scope) {
    $scope.data = 'user controller'
});

picload.controller('MediaController', function($scope) {
    $scope.data = 'media controller'
});

//
//
// picloadApp.factory('Data', function() {
//     return {'message':'Welcom to instagram loader apps'}
// });
//
// picloadApp.controller('ApiController', function (Data) {
//     $scope.method = "GET";
//     $scope.base_url = "https://api.instagram.com/v1/users/search?q=saruberoz&access_token=2265022.f59def8.f63bdd0b9bce4d008a7c0fabddd1d78a";
//
//     // $scope.access_token = "2265022.f59def8.f63bdd0b9bce4d008a7c0fabddd1d78a";
//     // $scope.url = $scope.base_url.concat(access_token);
//
//     $scope.fetch = function() {
//         $scope.code = null;
//         $scope.response = null;
//
//         $http({method: $scope.method, url: $scope.url, cache: $templateCache}).
//             success(function(data, status) {
//                 $scope.status = status;
//                 $scope.data = data;
//             }).
//             error(function(data, status) {
//                 $scope.data = data || "Request Failed";
//                 $scope.status = status;
//             });
//     };
//
//     // v1/users/search?q=jack&access_token=
// });
//
//
// //
// // CLIENT INFO
// // CLIENT ID	ea2ea54c662c4a8ba136adb5e2c25a7a
// // CLIENT SECRET	6ba5cd189f114dc9975596a10b2f76f0
// // WEBSITE URL	http://picload.herokuapp.com/
// // REDIRECT URI	http://picload.herokuapp.com/
//
//
// // 1. https://api.instagram.com/oaccount/accountorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=code
// https://api.instagram.com/oaccount/accountorize/?client_id=ea2ea54c662c4a8ba136adb5e2c25a7a&redirect_uri=http://picload.herokuapp.com&response_type=200

var myApp = angular.module('myApp', ['ngCart']);

myApp.controller('myCtrl', ['$scope', '$http', 'ngCart', function($scope, $http, ngCart) {
    ngCart.setTaxRate(24);
    ngCart.setShipping(0);

    $scope.item = {};

    $scope.$on('ngCart:itemAdded', function(ngCartItem){
      console.log('Hopa')
      $scope.item = {};
    });
}]);

var PloneConfTickets = angular.module('PloneConfTickets', ['ngCart']);

PloneConfTickets.controller('PloneConfTicketsCtrl', ['$scope', '$http', 'ngCart', function($scope, $http, ngCart) {
    ngCart.setTaxRate(24);
    ngCart.setShipping(0);

    $scope.price = 274.20;
    $scope.item = {};

    $scope.$on('ngCart:itemAdded', function(ngCartItem){
      $scope.item = {};
    });
}]);

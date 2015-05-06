var PloneConfTickets = angular.module('PloneConfTickets', ['ngCart']);

PloneConfTickets
  .controller('PloneConfTicketsCtrl', ['$scope', 'ngCart', '$locale', '$element', function ($scope, ngCart, $locale, $element) {
    $locale.NUMBER_FORMATS.CURRENCY_SYM = $element.data('currency') || '€';
    ngCart.setTaxRate($element.data('vat') || 24);
    ngCart.setShipping(0);

    $scope.price = $element.data('price') || 275;
    $scope.item = {};

    $scope.chartNotEmpty = function () {
      return ngCart.getTotalItems() ? true : false;
    };

    $scope.$on('ngCart:itemAdded', function () {
      $scope.item = {};
    });

    $scope.$on('ngCart:itemRemoved', function () {
      $scope.item = {};
    });

  }])

  .controller('PloneConfTicketsCart', ['$scope', 'ngCart', '$locale', '$element', '$http', function ($scope, ngCart, $locale, $element, $http) {
    $locale.NUMBER_FORMATS.CURRENCY_SYM = $element.data('currency') || '€';
    ngCart.setTaxRate($element.data('vat') || 24);
    ngCart.setShipping(0);

    $scope.price = $element.data('price') || 275;

    $scope.getCart = function () {
      var items = [];
      angular.forEach(ngCart.getItems(), function (item) {
        items.push(item.getData());
      });
      return items;
    };

    $scope.postData = false;
    $http.post('tickets.cart', {"cart": $scope.getCart()}).then(function (response) {
      $scope.postData = response.data;
    });

  }])

  .directive('uniqueEmail', ["ngCart", function (ngCart) {
    return {
      require: 'ngModel',
      link: function (scope, element, attrs, ctrl) {
        ctrl.$validators.uniqueEmail = function (modelValue) {
          return ngCart.getItemById(modelValue) ? false : true;
        };
      }
    };
  }]);

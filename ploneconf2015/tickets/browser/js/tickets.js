var PloneConfTickets = angular.module('PloneConfTickets', ['ngCart']);

PloneConfTickets
  .controller('PloneConfTicketsBuy', ['$scope', 'ngCart', '$locale', '$element', function ($scope, ngCart, $locale, $element) {
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

    $scope.getJSONCart = function () {
      return JSON.stringify( $scope.getCart() );
    };

    $scope.chartNotEmpty = function () {
      return ngCart.getTotalItems() ? true : false;
    };

    $scope.item = {};
    $scope.updateBilling = function () {
      if ($scope.chartNotEmpty()) {
        $scope.item = $scope.getCart()[0];
        $scope.item.name = $scope.item.firstName + " " + $scope.item.lastName;
      }
    };

    $scope.$on('ngCart:itemRemoved', function () {
      $scope.updateBilling();
    });

    $scope.updateBilling();
  }])

  .controller('PloneConfTicketsCheckout', ['$scope', 'ngCart', '$locale', '$element', '$http', function ($scope, ngCart, $locale, $element, $http) {
    //$scope.postData = false;
    //
    //$scope.getPostData = function () {
    //  $http.post('tickets.cart', {"cart": $scope.getCart()})
    //    .success(function (data) {
    //      if(data.AMOUNT) {
    //        $scope.postData = data;
    //      }else{
    //        $scope.postData = false;
    //      }
    //    })
    //    .error(function () {
    //      $scope.postData = false;
    //    });
    //};
    //
    //
    //$scope.$on('ngCart:itemRemoved', function () {
    //  $scope.getPostData();
    //});
    //
    //$scope.getPostData();
  }])

  .controller('PloneConfTicketsThanks', ['$scope', 'ngCart', '$locale', '$element', '$http', function ($scope, ngCart, $locale, $element, $http) {
    ngCart.empty();
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

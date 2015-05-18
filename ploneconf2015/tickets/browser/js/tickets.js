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

    $scope.updateBilling();
    $scope.$on('ngCart:itemRemoved', function () {
      $scope.updateBilling();
    });

    $scope.postData = false;
    $scope.checkoutClicked = false;
    $scope.submitCartForm = function () {
      $scope.checkoutClicked = true;
      $http.post('tickets.checkout', {"cart": $scope.getCart(), 'billing': $scope.item})
        .success(function (data) {
          if (data.AMOUNT) {
            $scope.postData = data;
            $scope.$broadcast('postDataReady');
          } else {
            $scope.postData = false;
          }
        })
        .error(function () {
          console.error("Eroare");
        });
      return false;
    };

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
  }])

  .directive('submitOn', function () {
    return {
        link: function(scope, elm, attrs) {
            scope.$on(attrs.submitOn, function() {
                //We can't trigger submit immediately,
                // or we get $digest already in progress error :-[
                // (because ng-submit does an $apply of its own)
                setTimeout(function () {
                    elm.trigger('submit');
                });
            });
        }
    };
});

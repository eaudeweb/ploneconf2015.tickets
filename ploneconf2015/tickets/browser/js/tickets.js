var PloneConfTickets = angular.module('PloneConfTickets', ['ngCart']);

PloneConfTickets
  .controller('PloneConfTicketsBuy', ['$scope', 'ngCart', 'store', '$locale', '$element', '$http', function ($scope, ngCart, store, $locale, $element, $http) {
    $locale.NUMBER_FORMATS.CURRENCY_SYM = $element.data('currency') || '€';
    var vat = $element.data('vat') || 24;
    vat = 1 + vat / 100;
    $scope.price = $element.data('price') || 275;
    $scope.price = $scope.price * vat;
    $scope.item = {};
    $scope.showNewTicketButton = false;

    $scope.cartNotEmpty = function () {
      return ngCart.getTotalItems() ? true : false;
    };

    if ($scope.cartNotEmpty()) {
      $scope.showNewTicketButton = true;
    }

    $scope.getCart = function () {
      var items = [];
      angular.forEach(ngCart.getItems(), function (item) {
        items.push(item.getData());
      });
      return items;
    };

    $scope.getJSONCart = function () {
      return JSON.stringify($scope.getCart());
    };


    $scope.billingItem = store.get('billingItem');

    $scope.updateBilling = function () {
      if (!$scope.billingItem) {
        if ($scope.cartNotEmpty()) {
          $scope.billingItem = $scope.getCart()[0];
          $scope.billingItem.name = $scope.billingItem.firstName + " " + $scope.billingItem.lastName;
          store.set('billingItem', JSON.stringify($scope.billingItem));
        }
      } else {
        store.set('billingItem', JSON.stringify($scope.billingItem));
      }
    };

    $scope.updateBilling();

    $scope.$on('ngCart:itemAdded', function () {
      $scope.item = {};
      $scope.showNewTicketButton = true;
      $scope.updateBilling();
    });

    $scope.$on('ngCart:itemRemoved', function () {
      $scope.item = {};
      if (!$scope.cartNotEmpty()) {
        $scope.showNewTicketButton = false;
      }
      $scope.updateBilling();
    });

    $scope.postData = false;
    $scope.checkoutClicked = false;
    $scope.submitCartForm = function () {
      $scope.checkoutClicked = true;
      $http.post('tickets.checkout', {"cart": $scope.getCart(), 'billing': $scope.billingItem})
        .success(function (data) {
          if (data.AMOUNT) {
            $scope.updateBilling();
            $scope.postData = data;
            $scope.$broadcast('postDataReady');
          } else {
            $scope.postData = false;
          }
        })
        .error(function () {
          $scope.postData = false;
          console.error("Eroare");
        });
      return false;
    };

  }])

  .controller('PloneConfTicketsThanks', ['$scope', 'ngCart', 'store', function ($scope, ngCart, store) {
    ngCart.empty();
    store.set('billingItem');
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
      link: function (scope, elm, attrs) {
        scope.$on(attrs.submitOn, function () {
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

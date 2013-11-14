'use strict';

var tornadoSkelControllers = angular.module('tornadoSkelControllers', []);

tornadoSkelControllers.controller('IndexCtrl', ['$scope',
    function($scope) {
        $scope.intro = 'This is our tornado+angularjs skeleton!';
    }
]);

'use strict';

var tornadoSkel = angular.module('tornadoSkel', [
    'ngRoute',
    'tornadoSkelControllers'
]);

tornadoSkel.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: 'static/partials/intro.html',
            controller: 'IndexCtrl'
        }).
        otherwise({
            redirectTo: '/'
        });
    }
]);

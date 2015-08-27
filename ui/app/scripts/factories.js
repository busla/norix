'use strict';
/*
 Factories 
 */

angular.module('idkendurApp')

.factory('Idkendur', function($resource) {
    return $resource('http://:ip:port/players/',  
    	{ port: ':5000', ip: 'localhost' }, 
    	{ 'query': {method: 'GET', isArray:false, params:{club:'@club',username:'@username',password:'@password'}}}
    );
});
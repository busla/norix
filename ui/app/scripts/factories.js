'use strict';
/*
 Factories 
 */

angular.module('idkendurApp')

.factory('Idkendur', function($resource) {
    return $resource('http://:ip:port/players/',  
    	{ port: ':5000', ip: '176.58.105.227' }, 
    	{ 'query': {method: 'GET', isArray:false, params:{club:'@club',username:'@username',password:'@password'}}}
    );
});
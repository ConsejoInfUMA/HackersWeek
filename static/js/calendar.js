(function(){
	var app = angular.module('home',[ ]);

	app.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol('{$');
	    $interpolateProvider.endSymbol('$}');
	});


	var activities = [
		'Conferencias',
		'Talleres',
		'Juegos',
		'Videojuegos'
	];

	var events = {"1": {"day_no": 1, "day_name": "Lunes", "stripes": {"1": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "10:30 - 11:30"}, "2": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "11:30 - 12:30"}, "3": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "12:30 - 15:30"}, "4": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "16:30 - 17:30"}, "5": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "17:30 - 18:30"}, "6": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "18:30 - 19:30"}}}, "2": {"day_no": 2, "day_name": "Martes", "stripes": {"1": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "10:30 - 11:30"}, "2": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "11:30 - 12:30"}, "3": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "12:30 - 15:30"}, "4": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "16:30 - 17:30"}, "5": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "17:30 - 18:30"}, "6": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "18:30 - 19:30"}}}, "3": {"day_no": 3, "day_name": "Mi\u00e9rcoles", "stripes": {"1": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "10:30 - 11:30"}, "2": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "11:30 - 12:30"}, "3": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "12:30 - 15:30"}, "4": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "16:30 - 17:30"}, "5": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "17:30 - 18:30"}, "6": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "18:30 - 19:30"}}}, "4": {"day_no": 4, "day_name": "Jueves", "stripes": {"1": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "10:30 - 11:30"}, "2": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "11:30 - 12:30"}, "3": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "12:30 - 15:30"}, "4": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "16:30 - 17:30"}, "5": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "17:30 - 18:30"}, "6": {"events": {"C": {"kind": "Conferencia", "data": {}}, "J": {"kind": "Juego", "data": {}}, "M": {"kind": "Miscelanea", "data": {}}, "W": {"kind": "Taller", "data": {}}}, "time": "18:30 - 19:30"}}}};

	app.controller('CalendarController', ['$http' ,function($http){

		var calendar = this;

		calendar.events = events;

		$http.get('/api/calendar/').success(function(response){
			calendar.events = response;
		});
		
		this.day = 1;
		this.activities = activities;

		this.getStripesFor = function(day){
			return this.events[day].stripes;
		};

		this.changeDay = function(day){
			this.day = day;
		};

		this.daySelected = function(day){
			return this.day === day;
		};

	} ]);

})();

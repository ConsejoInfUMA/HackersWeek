(function(){
	var app = angular.module('profile_details',[ ]);

	app.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol('{$');
	    $interpolateProvider.endSymbol('$}');
	});

	app.controller('FormController', function(){
		this.course = null;
		this.isETSII = function(){

			return this.course == "GII" || 
				   this.course == "GIS" ||
				   this.course == "GIC" ||
				   this.course == "GISa" ||
				   this.course == "II" ||
				   this.course == "ITS" ||
				   this.course == "ITG";
		};
	});


})();

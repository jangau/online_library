angular.module('booksOnline', []).controller('booksCtrl', function($scope, $http) {
	$scope.books = [
		{"title": "book1", "rating": "5"},
		{"title": "book2", "rating": "4"},
		{"title": "book3", "rating": "4.5"},
		{"title": "book4", "rating": "3.5"},
		{"title": "book5", "rating": "1"},
		{"title": "book6", "rating": "4"},
		{"title": "book7", "rating": "3"},
		{"title": "book8", "rating": "2"},
	];
	
	$scope.bindPicture = function() {
		for (i = 0; i< $scope.books.length; i++){
			$scope.books[i].image_path = "../book_covers/" + $scope.books[i].book_id + ".jpg";
		}
	}
	
	$scope.getFullStars = function(book) {
		return new Array(parseInt(book.rating));   
	}
	
	$scope.getHalfStars = function(book) {
		return new Array(5-parseInt(book.rating));
	}
	
	$scope.getBooks = function() {
		$http.get('/books/').then(
			function successCallback(response){
				$scope.books = response.data;
		},
			function errorCallback(response){
				$scope.books = [];
				console.log('error getting books list');
		})
	}
	
	$scope.getBooks();
	$scope.bindPicture();
	
})
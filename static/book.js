angular.module('booksOnline', []).controller('bookCtrl', function($scope) {
	$scope.book ={
		"title": "book1",
		"rating": "3",
		"image_path": "./larger_cover.jpg",
		"author": "some author",
		"genre": "adventure",
		"description": "This is the description for book1 and I'm just trying to fill a lot of text space so I'm going to repeat a word: word, word, word, word, word, word, word, word, word, word, word, word"
	};
	
	$scope.reviews = [
		{"text": "Very boring book, shame!", "rating": "1", "user": "Angry Joe"},
		{"text": "Great book!", "rating":"5", "user": "Happy Joe"}
	]
	
	$scope.getFullStars = function() {
		return new Array(parseInt($scope.book.rating));   
	}
	
	$scope.getHalfStars = function() {
		return new Array(5-parseInt($scope.book.rating));
	}
	
})
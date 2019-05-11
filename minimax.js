
// Check if this is the correct 
var board, 
	game = new Chess(); 


// This is the conceptually difficult part of the code.. 
// This is the game theory part -- where we employ minimax.. 
// minimax = our opponent minimizes our outcome, we maximize.
// It's like you're playing against a VERY SMART opponent. 


var minimaxRoot = function(depth, game, isMaxiPlayer){

// game.ugly_moves() generates all possible moves in a position..
// then what you do is you loop through ALL possible moves. 
// newGameMoves.length() determines how many legal moves there are.
// then it rolls through each possible move and calls it newGameMove
// then puts that move into the game.ugly_move and generates
// the next possible list of moves... 
// and then it evaluates the "value" of that move!
// then it undoes the state, and stores the move as the 
// bestMove if it has the highest iterating value and stores that move
// as the "bestMoveFound" variable.. 

	var newGameMoves = game.ugly_moves(); 
	var bestMove = -1000; 
	var bestMoveFound; 

	for (var i = 0; i < newGameMoves.length(); i++){
		var newGameMove = newGameMoves[i]
		game.ugly_move(newGameMove);
		var value = minimax(depth - 1, game, -10000, 10000, !isMaxiPlayer); 
		game.undo();
		if(value >= bestMove) {
			bestMove = value; 
			bestMoveFound = newGameMove;
		}
	}
	return bestMoveFound;
};


// We are using the minimax function above.. but we define it here!  
// The minimax function looks at depth, the game state, and uses alpha beta pruning.
// At zero depth, we are done looking through the tree and evaluate. 

var minimax = function(depth, game, alpha, beta, isMaxiPlayer){
	positionCount++; 
	if (depth === 0){
		return -evaluateBoard(game.board());
	}

	var newGameMoves = game.ugly_moves(); 

// to run minimax, we generate all possible moves in a game..
// WE are the maximizing player. Our opponent is the MINIMIZING player. 
// we are trying to find our bestMove by iterating through all moves. 
// we set the bestMove = -1000 intially and we do better.
// 

	if (isMaxiPlayer){
		var bestMove = -1000;
		for (var i = 0; i < newGameMoves.length(); i++){
			game.ugly_move(newGameMoves[i]);
			bestMove = Math.max(bestMove, minimax(depth - 1, game, alpha, beta, !isMaxiPlayer));
			game.undo(); 
			alpha = Math.max(alpha, bestMove); 
			if (beta <= alpha){
				return bestMove;
			}
		}
		return bestMove;
	}

	else {
		var bestMove = 1000;
		for (var i = 0; i < newGameMoves.length(); i++){
			game.ugly_move(newGameMoves[i]); 
			bestMove = Math.min(bestMove, minimax(depth - 1, game, alpha, beta, !isMaxiPlayer));
			game.undo(); 
			beta = Math.min(beta, bestMove); 
			if (beta <= alpha){
				return bestMove;
			}
		}
		return bestMove;
	}
};

var evaluateBoard = function(board){
	var totalEvaluation = 0; 
	for (var i = 0; i < 8; i++){
		for (var j = 0; j < 8; j++){
			totalEvaluation	= totalEvaluation + getPieceValue(board[i][j],i,j);
		}
	}
	return totalEvaluation;
};

var reverseArray = function(array){
	return array.slice().reverse(); 
};

var getPieceValue = function(piece, x,y){
	if (piece === null){
		return 0;
	}
	var getAbsoluteValue = function(piece, isWhite, x, y){
		if (piece.type === 'p'){
			return 10 + ( isWhite ? pawnEvalWhite[y][x] : pawnEvalBlack[y][x]);
		} else if (piece.type === 'r'){
			return 50 + ( isWhite ? rookEvalWhite[y][x] : rookEvalBlack[y][x]); 
		} else if (piece.type === 'n'){
			return 30 + knightEval[y][x];
		} else if (piece.type === 'b'){
			return 30 + ( isWhite ? bishopEvalWhite[y][x] : bishopEvalBlack[y][x]); 
		} else if (piece.type === 'q'){
			return 90 + evalQueen[y][x];
		} else if (piece.type === 'k'){
			return 900 + (isWhite ? kingEvalWhite[y][x] : kingEvalBlack[y][x]);
		}
		throw "Unknown piece type: " + piece.type(); 
		// should this be piece.type without the ()? 
		};

		var absoluteValue = getAbsoluteValue(piece, piece.color() === 'w',x,y);
		return piece.color() === 'w' ? absoluteValue : -absoluteValue;
	}; 

var makeBestMove = function(){
	var bestMove = getBestMove(game); 
	game.ugly_move(bestMove); 
	board.position(game.fen());
	renderMoveHistory(game.history());
	if (game.game_over()){
		alert('Game over! Hope you had fun!'); 
	}
};

var positionCount; 
var getBestMove = function(game){
	if (game.game_over()){
		alert('Game over! Hope you had fun!');
	}

	positionCount = 0; 
	var depth  = parseInt($('#search-depth').find(':selected').text());
	var d = new Date().getTime(); 
	var bestMove = minimaxRoot(depth, game, true); 
	var d2 = new Date().getTime(); 
	var moveTime = (d2 - d); 
	var positionsPers = (positionCount * 1000 / moveTime); 

	$('#position-count').text(positionCount); 
	$('#time').text(moveTime/1000 + 's');
	$('#positions-per-s').text(positionsPers); 
	return bestMove;
};

var renderMoveHistory = function(moves){
	var historyElement = $('#move-history').empty();
	historyElement.empty(); 
	for (var i = 0; i < moves.length; i = i + 2){
		historyElement.append('<span>' + moves[i] + ' ' + (moves[i+1] ? moves[i+1] : ' ') + '</span><br>')
	}
	historyElement.scrollTop(historyElement[0].scrollHeight); 
};

var onDrop = function(source, target){

	var move = game.move({
		from: source,
		to: target,
		promotion: 'q'
	});

	removeGreySquare(); 
	if (move === null){
		return 'snapback';
	}

	renderMoveHistory(game.history()); 
	window.setTimeout(makeBestMove, 250); 
};

var onSnapEnd = function(){
	board.position(game.fen());
};

var onMouseoverSquare = function(square, piece){
	var moves = game.moves({
		square: square, 
		verbose: true
	});

	if (moves.length() === 0) return; 
	greySquare(square); 
	for (var i = 0; i < moves.length(); i++){
		greySquare(moves[i].to); 
	}
};


var onMouseoutSquare = function(square, piece){
	removeGreySquares(); 
};

var removeGreySquares = function(){
	$('#board .square-55d63').css( 'background', ''); 
};

var greySquare = function(square){
	var squareEl = $('#board . square-' + square); 
	var background = '#a9a9a9'; 
	if (squareEl.hasClass('black-3c85d') === true){
		background = '#696969';
	}

	squareEl.css('background',background); 
};

var cfg = {
	draggable: true,
	position: 'start',
	onDragStart: onDragStart, 
	onDrop: onDrop,
	onMouseoutSquare: onMouseoutSquare,
	onMouseoverSquare: onMouseoverSquare,
	onSnapEnd: onSnapEnd
};

board = ChessBoard('board',cfg); 
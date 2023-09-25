from django.http import JsonResponse
from django.views import View
import json

from .chess_logic import get_piece_valid_moves

class GetValidMovesView(View):
    """
        This api is used to return the all valid positions of user input piece type
        params:
            piece_type: "Knight/Queen/Rook/Bishop"
            postions: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                                "Rook":"Position of rook" , "Knight":"Position of Knight"}
        """
    def get(self, request, piece_type):
        data = json.loads(request.body)
        pieces_position = data.get('postions')
        valid_moves = []
        if piece_type == 'queen' and pieces_position:
            valid_moves = get_piece_valid_moves("Queen" , pieces_position)
        elif piece_type == 'knight' and pieces_position:
            valid_moves = get_piece_valid_moves("Knight" , pieces_position)
        elif piece_type == 'rook' and pieces_position:
            valid_moves = get_piece_valid_moves("Rook" , pieces_position)
        elif piece_type == 'bishop' and pieces_position:
            valid_moves = get_piece_valid_moves("Bishop" , pieces_position)
        elif not pieces_position and not piece_type:
            return JsonResponse({'error': 'Invalid piece type or missing positions from request data'})
        return JsonResponse({'valid_moves': valid_moves})

def is_valid_position(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def get_knight_moves(row, col):
    """
    This function help us to return the valid positions of knight
        params:
        row: Row number where the knight are present
        column: column number where the knight are present
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    moves = []
    knight_direction = [
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    ]
    for r_offset, c_offset in knight_direction:
        new_row, new_col = row + r_offset, col + c_offset
        if is_valid_position(new_row, new_col):
            moves.append(f"{chr(new_col + ord('A'))}{new_row + 1}")
    return moves


def get_rook_moves(row, col, pieces_position):
    """
    This function help us to return the valid positions of rook
        params:
        row: Row number where the rook are present
        column: column number where the rook are present
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    moves = []
    rook_directions = [
        (-1, 0),  # Up
        (0, -1),  # Left
        (0, 1),  # Right
        (1, 0),  # Down
    ]
    break_outer = False
    for r_offset, c_offset in rook_directions:
        new_row, new_col = row + r_offset, col + c_offset
        while is_valid_position(new_row, new_col):
            target_position = f"{chr(new_col + ord('A'))}{new_row + 1}"
            for piece_position in pieces_position.values():
                if target_position == piece_position:
                    break_outer = True  # Set the flag to break both loops
                    moves.append(f"{chr(new_col + ord('A'))}{new_row + 1}")
                    break  # Stop if any piece is encountered
            moves.append(f"{chr(new_col + ord('A'))}{new_row + 1}")
            new_row += r_offset
            new_col += c_offset
    return moves


def get_bishop_moves(row, col, pieces_position):
    """
    This function help us to return the valid positions of bishop
        params:
        row: Row number where the bishop are present
        column: column number where the bishop are present
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    moves = []
    bishop_directions = [
        (-1, -1),  # Diagonal Up-Left
        (-1, 1),  # Diagonal Up-Right
        (1, -1),  # Diagonal Down-Left
        (1, 1),  # Diagonal Down-Right
    ]
    break_outer = False
    for r_offset, c_offset in bishop_directions:
        new_row, new_col = row + r_offset, col + c_offset
        while is_valid_position(new_row, new_col):
            target_position = f"{chr(new_col + ord('A'))}{ new_row + 1}"
            for piece_position in pieces_position.values():
                if target_position == piece_position:
                    break_outer = True  # Set the flag to break both loops
                    moves.append(f"{chr(new_col + ord('A'))}{new_row + 1}")
                    break  # Stop if any piece is encountered
            moves.append(f"{chr(new_col + ord('A'))}{new_row + 1}")
            new_row += r_offset
            new_col += c_offset
    return moves


def get_queen_moves(row, col, pieces_position):
    """
    This function help us to return the valid positions of queen
        params:
        row: Row number where the queen are present
        column: column number where the queen are present
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    moves = get_bishop_moves(row, col, pieces_position) + get_rook_moves(
        row, col, pieces_position
    )
    return moves


def get_valid_moves_for_one_piece(
    piece_type, single_piece_position, all_pieces_position
):
    """
    This function help us to return the valid positions of single piece
        params:
        piece_type: "Knight/Queen/Rook/Bishop"
        piece_position: "The position of the that single piece"
        row: Row number where the piece are present
        column: column number where the piece are present
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    moves = []
    if piece_type == "Knight":
        row, col = int(single_piece_position[1]) - 1, ord(
            single_piece_position[0]
        ) - ord("A")
        moves = get_knight_moves(row, col)
    elif piece_type == "Queen":
        row, col = int(single_piece_position[1]) - 1, ord(
            single_piece_position[0]
        ) - ord("A")
        moves = get_queen_moves(row, col, all_pieces_position)
    elif piece_type == "Bishop":
        row, col = int(single_piece_position[1]) - 1, ord(
            single_piece_position[0]
        ) - ord("A")
        moves = get_bishop_moves(row, col, all_pieces_position)
    elif piece_type == "Rook":
        row, col = int(single_piece_position[1]) - 1, ord(
            single_piece_position[0]
        ) - ord("A")
        moves = get_rook_moves(row, col, all_pieces_position)
    return moves


def get_all_pieces_valid_moves(pieces_position):
    # Calculate valid moves for all pices
    """
    This function help us to return the all pieces valid positions only
    params:
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                        "Rook":"Position of rook" , "Knight":"Position of Knight"}

    """

    knight_piece_type = "Knight"
    knight_piece_position = pieces_position[knight_piece_type]
    knight_valid_moves = get_valid_moves_for_one_piece(
        knight_piece_type, knight_piece_position, pieces_position
    )

    rook_piece_type = "Rook"
    rook_piece_position = pieces_position[rook_piece_type]
    rook_valid_moves = get_valid_moves_for_one_piece(
        rook_piece_type, rook_piece_position, pieces_position
    )

    queen_piece_type = "Queen"
    queen_piece_position = pieces_position[queen_piece_type]
    queen_valid_moves = get_valid_moves_for_one_piece(
        queen_piece_type, queen_piece_position, pieces_position
    )

    bishop_piece_type = "Bishop"
    bishop_piece_position = pieces_position[bishop_piece_type]
    bishop_valid_moves = get_valid_moves_for_one_piece(
        bishop_piece_type, bishop_piece_position, pieces_position
    )

    return knight_valid_moves, rook_valid_moves, queen_valid_moves, bishop_valid_moves


def get_piece_valid_moves(piece_type, pieces_position):
    """
    This function help us to return the all valid positions of user input piece
    params:
        piece_type: "Knight/Queen/Rook/Bishop"
        pieces_position: {"Queen":"Position of queen" , "Bishop":"Position of bishop" ,
                            "Rook":"Position of rook" , "Knight":"Position of Knight"}
    """
    target_piece_moves = []
    all_pieces_moves = []
    (
        knight_valid_moves,
        rook_valid_moves,
        queen_valid_moves,
        bishop_valid_moves,
    ) = get_all_pieces_valid_moves(pieces_position)
    if piece_type == "Knight":
        all_pieces_moves = rook_valid_moves + queen_valid_moves + bishop_valid_moves
        target_piece_moves = knight_valid_moves
    elif piece_type == "Queen":
        all_pieces_moves = rook_valid_moves + knight_valid_moves + bishop_valid_moves
        target_piece_moves = queen_valid_moves
    elif piece_type == "Bishop":
        all_pieces_moves = rook_valid_moves + queen_valid_moves + knight_valid_moves
        target_piece_moves = bishop_valid_moves
    elif piece_type == "Rook":
        all_pieces_moves = knight_valid_moves + queen_valid_moves + bishop_valid_moves
        target_piece_moves = rook_valid_moves

    return list(set([
        iteration
        for iteration in target_piece_moves
        if iteration not in all_pieces_moves
    ]))

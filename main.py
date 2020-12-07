import pygame
import pygsheets

TILESIZE = 15
BOARD_POS = (10, 10)


def create_board_surf():
    board_surf = pygame.Surface((TILESIZE * 40, TILESIZE * 40))
    for y in range(40):
        for x in range(40):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('white'), rect)
    return board_surf


def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return (board[y][x], x, y)
    except IndexError:
        pass
    return None, None, None


def create_board():
    board = []
    for y in range(40):
        board.append([])
        for x in range(40):
            board[y].append(None)

    for x in range(0, 39):
        board[1][x] = ('black', 'pawn', x)

    return board


def draw_pieces(screen, board, font, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(40):
        for x in range(40):
            piece = board[y][x]
            if piece:
                selected = x == sx and y == sy
                color, type, index = piece
                s1 = font.render(type[0], True, pygame.Color('black' if selected else color))
                s2 = font.render(type[0], True, pygame.Color('darkgrey'))
                pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE + 1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center=pos.center))


def draw_selector(screen, piece, x, y):
    if piece != None:
        rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, board, selected_piece, font):
    if selected_piece:
        piece, x, y = get_square_under_mouse(board)
        if x != None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, type, index = selected_piece[0]
        s1 = font.render(type[0], True, pygame.Color(color))
        s2 = font.render(type[0], True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * TILESIZE,
                                    BOARD_POS[1] + selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
        # pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        # print(piece,x,y)
        return (x, y)

# set btn text
def text_objects(text, font):
    textSurface = font.render(text, True, [0, 0, 0])
    return textSurface, textSurface.get_rect()


# upload data to Google spreadsheet
# def upload_data(data):
#     columns = ["index", "x", "y"]
#
#     gc = pygsheets.authorize(service_file='ref/client_secret.json')
#     sh = gc.open('NTU_rating')
#     wks = sh[0]
#     wks = sh.worksheet_by_title('data')
#
#     cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
#     last_row = len(cells)
#
#     if len(wks.get_as_df()) == 0:
#         wks.insert_rows(row=0, number=1, values=columns)
#         wks.insert_rows(last_row, number=1, values=data)
#     else:
#         wks.insert_rows(last_row, number=1, values=data)

def main():
    pygame.init()
    font = pygame.font.SysFont('', 32)  # regular
    font_small = pygame.font.SysFont('', 26)  # small font
    screen = pygame.display.set_mode((600, 600))
    board = create_board()
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None

    # object locations
    blocklist = {}

    while True:
        piece, x, y = get_square_under_mouse(board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, x, y

                # upload data to Google spreadsheet
                # if e.button == 1:
                #     if button.collidepoint(e.pos):
                #         data = []
                #         for k, v in blocklist.items():
                #             item = [k, v[0], v[1]]
                #             data.append(item)
                #         upload_data(data)

            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos != None:
                    piece, old_x, old_y = selected_piece
                    board[old_y][old_x] = 0
                    new_x, new_y = drop_pos
                    board[new_y][new_x] = piece

                    # record object location
                    try:
                        blocklist[selected_piece[1]] = drop_pos
                    except:
                        blocklist[selected_piece[1]] = (0, 0)
                        blocklist[selected_piece[1]] = drop_pos

                selected_piece = None
                drop_pos = None

        screen.fill(pygame.Color('grey'))
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, font, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)

        # draw button
        button = pygame.Rect(270, 560, 60, 25)
        pygame.draw.rect(screen, [160, 160, 160], button)

        textSurf, textRect = text_objects("Submit", font_small)
        textRect.center = ((280 + (40 / 2)), (563 + (20 / 2)))
        screen.blit(textSurf, textRect)


        pygame.display.flip()
        clock.tick(10)



if __name__ == '__main__':
    main()


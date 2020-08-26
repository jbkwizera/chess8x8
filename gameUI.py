
from board import Board, Piece
import tkinter as tk
from tkinter import font, PhotoImage
from PIL import ImageTk, Image

class BoardUI(Board):
    src = None
    src_color = None
    dst_color = None
    def __init__(self):
        super().__init__()
        #---------------------------------main frame-----------------------------------
        root = tk.Tk()
        root.title('CHEESE')
        root.configure(bg='lightgray')
        self._main = tk.Frame(master=root, bg='lightgray')
        self._main.configure(bg='lightgray')
        self._theme_main = 'bisque4'
        self._theme_shad_ligt_w = 'darkseagreen1'
        self._theme_shad_ligt_b = 'darkseagreen2'
        self._theme_shad_dark_w = 'darkseagreen3'
        self._theme_shad_dark_b = 'darkseagreen4'

        #---------------------------------icon imges-----------------------------------
        icons = [['Rb.gif', 'Nb.gif', 'Bb.gif', 'Qb.gif', 'Kb.gif', 'Bb.gif', 'Nb.gif', 'Rb.gif'],
                 ['Rw.gif', 'Nw.gif', 'Bw.gif', 'Qw.gif', 'Kw.gif', 'Bw.gif', 'Nw.gif', 'Rw.gif']]

        blackp = []
        whitep = []
        for i in range(8):
            imgb = ImageTk.PhotoImage(Image.open('./pieces/gif/{}'.format(icons[0][i])).resize((70, 70)))
            imgw = ImageTk.PhotoImage(Image.open('./pieces/gif/{}'.format(icons[1][i])).resize((70, 70)))
            blackp.append(imgb)
            whitep.append(imgw)
        for i in range(8):
            imgb = ImageTk.PhotoImage(Image.open('./pieces/gif/Pb.gif').resize((70, 70)))
            imgw = ImageTk.PhotoImage(Image.open('./pieces/gif/Pw.gif').resize((70, 70)))
            blackp.append(imgb)
            whitep.append(imgw)

        #------------------------------populate board----------------------------------
        board_frm  = tk.Frame(master=self._main, relief=tk.RAISED, borderwidth=1, bg='lightgray')
        board_frm.pack(padx=15, pady=15)
        self._cells_lbls = []

        fill_clr = self._theme_main
        for i in range(8):
            row_lbls = []
            for j in range(8):
                cell_frm = tk.Frame(master=board_frm, height=80, width=80, relief=tk.RAISED, borderwidth=1, cursor='hand', bg=fill_clr)
                cell_lbl = tk.Label(master=cell_frm, width=80, height=80, bg=fill_clr)

                fill_clr = self._theme_main if fill_clr=='white' else 'white'
                cell_frm.message = 8*i + j              # cell id: 0...63
                cell_lbl.message = 8*i + j
                cell_lbl.bind('<Button-1>', self.perform_move)  # play on click
                cell_lbl.place(x=40, y=40, anchor='center')

                cell_frm.grid(row=i, column=j)
                cell_frm.pack_propagate(0)
                cell_frm.update()
                row_lbls.append(cell_lbl)
            self._cells_lbls.append(row_lbls)
            fill_clr = self._theme_main if fill_clr=='white' else 'white'

        #--------------------------------set image icons---------------------------------
        for n in range(16):
            i, j = n // 8, n % 8
            self._cells_lbls[i][j].configure(image=blackp[n])
            self._cells_lbls[6+i][j].configure(image=whitep[15-n])
        self._cells_lbls[7][3].configure(image=whitep[3])
        self._cells_lbls[7][4].configure(image=whitep[4])

        # launch gui
        self._main.pack(padx=16, pady=16)
        root.mainloop()

    def perform_move(self, event):
        location = int(event.widget.message)
        i = location //8
        j = location % 8
        print('clicked', self._board[i][j], i, j)
        for item in self._board[i][j]._status:
            if item != 'last_move':
                print(item, end=': ')
                for elem in self._board[i][j]._status[item]:
                    print(elem, end=' ')
                print()

        def unshade_move(src, dst):
            src = self._move_log[-1]['src']
            dst = self._move_log[-1]['dst']
            print(src, dst)
            self._cells_lbls[src[0]][src[1]].configure(bg=self.__class__.src_color)
            self._cells_lbls[dst[0]][dst[1]].configure(bg=self.__class__.dst_color)

        #-----------------------------move pieces ui-logic--------------------------------
        if not self.__class__.src:
            if self._player != self._board[i][j]._color:
                return
            if self._move_log[0]['last_was_full_move']:
                unshade_move(self._move_log[-1]['src'], self._move_log[-1]['dst'])

            if self._board[i][j]._name:
                self.__class__.src = (i, j)
                self.__class__.src_color = self._cells_lbls[i][j].cget('bg')
                self._cells_lbls[i][j].configure(bg=self._theme_shad_dark_w if self.__class__.src_color=='white' else self._theme_shad_dark_b)
                self._move_log[0]['last_was_full_move'] = False

        elif self.__class__.src:
            if self.is_valid_move(self.__class__.src, (i, j)):
                if self._move_log[0]['last_was_full_move']:
                    unshade_move(self._move_log[-1]['src'], self._move_log[-1]['dst'])
                src = self.__class__.src
                dst = (i, j)
                self._move_log.append({'src_piece': self._board[src[0]][src[1]],
                                       'dst_piece': self._board[dst[0]][dst[1]],
                                       'src': src, 'dst': dst})
                if self.is_valid_castle(src, dst):
                    # move the rook and clear
                    ri, rf = (0, 3) if dst[1] == 2 else (7, 5)
                    self._board[dst[0]][rf] = self._board[dst[0]][7] if dst[1] != 2 else self._board[dst[0]][0]
                    self._board[dst[0]][ri] = Piece(name='', color='', location=None)
                    self._cells_lbls[dst[0]][rf].configure(image=self._cells_lbls[dst[0]][ri].cget('image'))
                    self._cells_lbls[dst[0]][ri].configure(image='')
                    self.update_attacking_defending((dst[0], rf))
                    self.update_attacking_defending(dst)
                    self.update_attackers_defenders((dst[0], rf))
                    self.update_attackers_defenders(dst)

                # move clicked piece and clear
                self._board[dst[0]][dst[1]] = self._board[src[0]][src[1]]
                self._board[src[0]][src[1]] = Piece(name='', color='', location=None)
                self._cells_lbls[dst[0]][dst[1]].configure(image=self._cells_lbls[src[0]][src[1]].cget('image'))
                self._cells_lbls[src[0]][src[1]].configure(image='')
                self.update_attacking_defending(src)
                self.update_attacking_defending(dst)
                self.update_attackers_defenders(src)
                self.update_attackers_defenders(dst)

                # keep last move
                self._board[src[0]][src[1]]._status['last_move'] = [src, dst]
                if self._board[dst[0]][dst[1]]._name:
                    self._board[dst[0]][dst[1]]._status['last_move'] = [None, None]

                # shade
                self.__class__.dst_color = self._cells_lbls[dst[0]][dst[1]].cget('bg')
                self._cells_lbls[src[0]][src[1]].configure(bg=self._theme_shad_ligt_w if self.__class__.src_color=='white' else self._theme_shad_ligt_b)
                self._cells_lbls[dst[0]][dst[1]].configure(bg=self._theme_shad_ligt_w if self.__class__.dst_color=='white' else self._theme_shad_ligt_b)
                self._move_log[0]['last_was_full_move'] = True

                # destroy move
                self.__class__.src = None
                self._player = 'b' if self._player == 'w' else 'w'
                for move in self._move_log[1:]:
                    print('{:>2s} {:>2s} {:>s} {:>s}'.format(str(move['src_piece']), str(move['dst_piece']), str(move['src']), str(move['dst'])))
            else:
                if self._move_log[0]['last_was_full_move']:
                    unshade_move(self._move_log[-1]['src'], self._move_log[-1]['dst'])
                else:
                    shd = self.__class__.src
                    self._cells_lbls[shd[0]][shd[1]].configure(bg=self.__class__.src_color)

                self.__class__.src = (i, j) if self._board[i][j]._name else None # update move
                self._move_log[0]['last_was_full_move'] = False
                if self.__class__.src:
                    self.__class__.src_color = self._cells_lbls[i][j].cget('bg')
                    self._cells_lbls[i][j].configure(bg=self._theme_shad_dark_w if self.__class__.src_color=='white' else self._theme_shad_dark_b)


if __name__ == '__main__':
    BoardUI()

import urllib.request
import numpy as np

from bs4 import BeautifulSoup


# difficulty: [1,2,3,4] [easy, med, hard, vhard]
# puzzle_no: [1, 2, 3, ..., ?]
# size: [6, 8, 10, 12, 14]
def scrape_board(difficulty, puzzle_no, n):
    link = f'http://www.binarypuzzle.com/puzzles.php?size={size}&level={difficulty}&nr={puzzle_no}'
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    cells = soup.findAll('div', attrs={'class': 'puzzlecel'})

    board = np.repeat('_', n * n).reshape(n, n)

    k = 0
    for i in range(n):
        for j in range(n):
            cell = cells[k].text.strip()
            board[i][j] = cell if cell else '_'
            k += 1

    return board
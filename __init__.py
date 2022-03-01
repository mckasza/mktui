import sys
import time

# Control sequence introducer
csi = chr(0x1B)+'['

class Application:
    def __init__(self):
        self.children = []
        self.sequence_queue = ''

        sys.stdout.write(csi+'?1049h'+csi+'?25l')
        sys.stdout.flush()
    def update(self):
        for child in self.children:
            self.sequence_queue += child.draw()

        sys.stdout.write(self.sequence_queue)
        sys.stdout.flush()
        self.sequence_queue = ''
    def add_child(self, child):
        self.children.append(child)
    def mainloop(self):
        try:
            while True:
                self.update()
                time.sleep(0.1)
        except KeyboardInterrupt:
            sys.stdout.write(csi+'?1049l'+csi+'?25h')
            sys.stdout.flush()

class Window:
    def __init__(self, x, y, size_x, size_y, title='Window Title'):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.title = title
    def draw(self):
        sequence = ''
        
        sequence += csi+f'37;42m'
        for i in range(self.y, self.y+self.size_y):
            for j in range(self.x, self.x+self.size_x):
                sequence += csi+f'{i};{j}H'

                if i == self.y and j == self.x:
                    sequence += '\u250F'
                elif i == self.y and j == self.x+self.size_x-1:
                    sequence += '\u2513'
                elif i == self.y+self.size_y-1 and j == self.x+self.size_x-1:
                    sequence += '\u251B'
                elif i == self.y+self.size_y-1 and j == self.x:
                    sequence += '\u2517'
                elif i == self.y or i == self.y+self.size_y-1:
                    sequence += '\u2501'
                elif j == self.x or j == self.x+self.size_x-1:
                    sequence += '\u2503'
                else:
                    sequence += ' '
        sequence += csi+'0m'

        return sequence
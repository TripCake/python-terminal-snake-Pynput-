import shutil, time, random, sys, termios, tty, os, select

class TerminalGrid():
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.counter = 0
        self.length = 10
        self.running = True
        self.position = [5, 6]
        self.direction = None
        self.pos_history = []
        self.grid = [[' ' for x in range(grid_size[1])] for x in range(grid_size[0])]
        self.all_positions = [[x+1,y] for x in range(grid_size[0]-1) for y in range(0, grid_size[1], 2)]
        self.heads = {"right" : ">","left" : "<","up" : "^","down" : "v"}
    
    def move_write_flush(self, to_write, x, y):
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        sys.stdout.write(to_write)
        sys.stdout.flush()
        
    def generate_apple(self):
        padding = self.grid_size[1] - len('Your length is: '+str(self.length))
        menu = 'WASD: Move | Q: Quit '
        self.move_write_flush("\033[0m\033[48;5;231;38;5;0m"+"Your length is:"+" \033[1m"+str(self.length)+' ' * (padding-(len(menu)))+menu+"\033[0m",0,0)
        valid_positions = [position for position in self.all_positions if position not in self.pos_history]
        self.apple_pos = random.choice(valid_positions)
        self.move_write_flush("\033[1m"+"a"+"\033[0m", self.apple_pos[1], self.apple_pos[0],)
    
    def exit(self):
        self.running = False
        sys.stdout.write("\033[?25h")
        self.move_write_flush("~~~~~ GAME OVER ~~~~~~",self.grid_size[1]//2,self.grid_size[0]//2)
        time.sleep(2)
        os.system('clear')

    def snake(self):
        if self.direction == None:
            return
        if self.direction == 'right':
            self.position[1] += 2
        elif self.direction == 'left':
            self.position[1] -= 2
        elif self.direction == 'up':
            self.position[0] -= 1
        elif self.direction == 'down':
            self.position[0] += 1

        if self.position == self.apple_pos:
            self.length += 10
            self.generate_apple()
        elif self.position in self.pos_history[1:] or self.position not in self.all_positions:
            self.exit()
            return
        
        head = str(self.heads[self.direction])
        self.move_write_flush(f"\033[0m"+head,self.position[1],self.position[0])
        self.pos_history.append(list(self.position))
        try:
            self.move_write_flush("\033[0m"+"o"+"\033[0m",self.pos_history[-2][1], self.pos_history[-2][0])
        except:
            pass
        if len(self.pos_history) > self.length:
            self.move_write_flush(" ",self.pos_history[0][1],self.pos_history[0][0])
            del self.pos_history[:-self.length]
        
    def print_grid(self):
        os.system('clear')
        sys.stdout.write("\033[?25l")
        for row in self.grid:
                print(''.join(row))

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            if select.select([sys.stdin], [], [], 0.12)[0]:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def run(self):
        self.print_grid()
        self.generate_apple()
        while self.running:
            key = self.get_key()
            if key == 'q':
                sys.stdout.write("\033[?25h")
                os.system('clear')
                quit()
            if key == 'd' and self.direction != 'left':
                self.direction = 'right'
            if key == 'a' and self.direction != 'right':
                self.direction = 'left'
            if key == 'w' and self.direction != 'down':
                self.direction = 'up'
            if key == 's' and self.direction != 'up':
                self.direction = 'down'
            self.snake()

def start():
    size = shutil.get_terminal_size()
    thing = TerminalGrid([size.lines-1,size.columns])
    while True:
        thing.run()

if __name__ == '__main__':
    start()
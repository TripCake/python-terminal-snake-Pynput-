import shutil, time, random, os, sys
from pynput.keyboard import Listener, Key, KeyCode

class TerminalGrid():
    def __init__(self, grid_size, listener):
        self.grid_size = grid_size
        self.listener = listener
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
        menu = 'Q: Quit '
        self.move_write_flush("\033[0m\033[48;5;231;38;5;0m"+"Your length is:"+" \033[1m"+str(self.length)+' ' * (padding-(len(menu)))+menu+"\033[0m",0,0)
        valid_positions = [position for position in self.all_positions if position not in self.pos_history]
        self.apple_pos = random.choice(valid_positions)
        self.move_write_flush("\033[1m"+"a"+"\033[0m", self.apple_pos[1], self.apple_pos[0],)
    
    def exit(self):
        self.running = False
        self.listener.stop()
        sys.stdout.write("\033[?25h")
        self.move_write_flush("~~~~~ GAME OVER ~~~~~~",self.grid_size[1]//2,self.grid_size[0]//2)
        time.sleep(2)
        os.system('cls')
        start()

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
        os.system('cls')
        sys.stdout.write("\033[?25l")
        for row in self.grid:
                print(''.join(row))

    def run(self):
        self.print_grid()
        self.generate_apple()
        while self.running:
            self.counter += 1
            if self.counter > 10:
                self.snake()
                self.counter = 0
            time.sleep(0.006)

def start():
    def on_press(key):
        if key == KeyCode(char='q'):
            thing.running = False
            listener.stop()
            sys.stdout.write("\033[?25h")
            os.system('cls')
            quit()
        if key == Key.left and thing.direction != 'right':
            thing.direction = 'left'
        if key == Key.up and thing.direction != 'down':
            thing.direction = 'up'
        if key == Key.down and thing.direction != 'up':
            thing.direction = 'down'
        if key == Key.right and thing.direction != 'left':
            thing.direction = 'right'
    with Listener(on_press=on_press) as listener:
        size = shutil.get_terminal_size()
        thing = TerminalGrid([size.lines-1,size.columns], listener)
        thing.run()
        listener.join()

if __name__ == '__main__':
    start()
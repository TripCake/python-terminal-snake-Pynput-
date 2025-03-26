import platform

if platform.system() == 'Windows':
    import WindowsSnake as WindowsSnake
    WindowsSnake.start()
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    import UnixSnake as UnixSnake
    UnixSnake.start()
else:
    import PynputSnakeXpltfm
    PynputSnakeXpltfm.start()
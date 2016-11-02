import pygame
import sys

class GetKeys:
    def __init__(self, root):
        self.root = root
        pygame.init()
        ## start looking for events
        self.root.after(0, self.find_events)

    def find_events(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN and down==false:
                if event.key==K_w:#moves banshee up if w pressed, same for the other WASD keys below
                    
                elif event.key==K_a:
                    
                elif event.key==K_d:
                    
                elif event.key==K_s:
                    
           elif event.type==KEYUP:
                if event.key==K_w:#moves banshee up if w pressed, same for the other WASD keys below
                    
                elif event.key==K_a:
                    
                elif event.key==K_d:
                    
                elif event.key==K_s:
                    

        ## return to check for more events in a moment
        self.root.after(20, self.find_events)

    ## quit out of everything
    def quit(self):
        sys.exit()

def main():
    ## Tkinter initialization
    root = Tk()
    app = GetKeys(root)
    # get out by closing the window or pressing Control-q
    root.protocol('WM_DELETE_WINDOW', app.quit)
    root.bind('<Control-q>', app.quit)
    root.bind('<Control-Q>', app.quit)
    root.mainloop()

if __name__ == "__main__":
    main()
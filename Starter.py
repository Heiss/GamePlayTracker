from ProcessSearcher import ProcessSearcher

class Tracker():
    pr = None
    isRunning = True

    def __init__(self):
        self.pr = ProcessSearcher()
        
        while self.isRunning:
            self.loop()
    
    def loop(self):
        self.pr.loop()

if __name__ == '__main__':
    Tracker()

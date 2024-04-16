import random
from statistics import mode
from collections import deque, defaultdict

class BeautyContestGame:

    def __init__(self, low: int, high: int, mid: int, random: int, walk: int, learn: int, copy: int) -> None:
        self.playerCount = low + high + mid + random + walk + learn + copy
        self.players = []
        # cache 50 most previous winners in double ended queue
        self.winnerCache = deque()
        # cache all guesses from last in order
        self.lastCache = []
        self.it = 0
        for _ in range(low):
            self.players.append([0, "low"])

        for _ in range(high):
            self.players.append([0, "high"])

        for _ in range(mid):
            self.players.append([0, "mid"])

        for _ in range(random):
            self.players.append([0, "random"])

        for _ in range(walk):
            self.players.append([0, "walk"])

        for _ in range(learn):
            self.players.append([0, "learn"])

        for _ in range(copy):
            self.players.append([0, "copy"])

    def getWinner(self):
        totGuess = 0
        currCacheIdx = 0

        for i in range(len(self.players)):
            if self.players[i][1] == "low":
                self.players[i][0] = self.lowStrategy(currCacheIdx)

            elif self.players[i][1] == "high":
                self.players[i][0] = self.highStrategy(currCacheIdx)

            elif self.players[i][1] == "mid":
                self.players[i][0] = self.midStrategy(currCacheIdx)

            elif self.players[i][1] == "random":
                self.players[i][0] = self.randomStrategy(currCacheIdx)

            elif self.players[i][1] == "walk":
                self.players[i][0] = self.walkStrategy(currCacheIdx)

            elif self.players[i][1] == "learn":
                self.players[i][0] = self.learningStrategy(currCacheIdx)

            elif self.players[i][1] == "copy":
                self.players[i][0] = self.copyStrategy(currCacheIdx)

            currCacheIdx += 1
            totGuess += self.players[i][0]
        avgGuess = totGuess / self.playerCount
        return int((2/3) * avgGuess)
    
    # Types of Strategies That May Be Employed

    # Random Strategy - Random guess between 0 and 100
    def randomStrategy(self, cache):
        if not self.it:
            self.lastCache.append(random.randint(0, 1000))
            return self.lastCache[-1]
        else:
            self.lastCache[cache] = random.randint(0, 1000)
            return self.lastCache[cache]
    
    # Low Strategy - Random guess between 0 and 33
    def lowStrategy(self, cache):
        if not self.it:
            self.lastCache.append(random.randint(0, 333))
            return self.lastCache[-1]
        else:
            self.lastCache[cache] = random.randint(0, 333)
            return self.lastCache[cache]

    # High Strategy - Random guess between 67 and 100
    def highStrategy(self, cache):
        if not self.it:
            self.lastCache.append(random.randint(667, 1000))
            return self.lastCache[-1]
        else:
            self.lastCache[cache] = random.randint(667, 1000)
            return self.lastCache[cache]

    # Mid Strategy - Random guess between 34 and 66
    def midStrategy(self, cache):
        if not self.it:
            self.lastCache.append(random.randint(334, 666))
            return self.lastCache[-1]
        else:
            self.lastCache[cache] = random.randint(334, 666)
            return self.lastCache[cache]

    # Advanced Strategies

    # Random Walk Strategy - Random guess between 0 and 100 upon first iteration
    # Guess increases or decreases each iteration thereafter based on prev winner
    def walkStrategy(self, walkNum: int):
        if not self.it:
            self.randomStrategy(walkNum)
            return self.lastCache[-1]
        else:
            diff = abs(self.lastCache[walkNum] - self.winnerCache[-1][0])
            if self.lastCache[walkNum] > self.winnerCache[-1][0]:
                if (random.randint(0,1)):
                    self.lastCache[walkNum] -= (diff // 2)
                else:
                    self.lastCache[walkNum] -= (diff // 4)
            elif self.lastCache[walkNum] < self.winnerCache[-1][0]:
                if (random.randint(0,1)):
                    self.lastCache[walkNum] += (diff // 2)
                else:
                    self.lastCache[walkNum] += (diff // 4)
            return self.lastCache[walkNum]

    # Learning Strategy - Players adjust strategy based on stragies that have won the most
    # in previous rounds
    def learningStrategy(self, cache: int):
        if not self.it:
            self.randomStrategy(cache)
            return self.lastCache[-1]
        else:
            d = defaultdict(int)
            for guess, strategy in self.winnerCache:
                d[strategy] += 1
            v = list(d.values())
            k = list(d.keys())
            mostWon = k[v.index(max(v))]
            if mostWon == "low":
                self.lowStrategy(cache)
            elif mostWon == "high":
                self.highStrategy(cache)
            elif mostWon == "mid":
                self.midStrategy(cache)             
            elif mostWon == "random":
                self.randomStrategy(cache)     
            elif mostWon == "walk":
                self.walkStrategy(cache)
            else:
                self.walkStrategy(cache)
            return self.lastCache[cache]

    # Copy Strategy - Players copy a guess that was successful in previous rounds
    def copyStrategy(self, cache: int):
        if not self.it:
            self.randomStrategy(cache)
            return self.lastCache[-1]
        else:
            x = random.randint(0, len(self.winnerCache) - 1)
            self.lastCache[cache] = self.winnerCache[x][0]
            return self.lastCache[cache]

    
    def simRound(self):
        winningNum = self.getWinner()
        closest = 1000
        winner = 1000
        for guess, strategy in self.players:
            if abs(winningNum - guess) < closest:
                closest = abs(winningNum - guess)
                winner = [guess, strategy]
        if len(self.winnerCache) >= 10:
            self.winnerCache.popleft()
        self.winnerCache.append(winner)
        self.it += 1
        print(self.winnerCache)
        print("------")
        return winner

numIt = 1000
game = BeautyContestGame(low=100, high=500, mid=50, random=50, walk=100, learn=100, copy=100)
winners = []
for _ in range(numIt):
    winners.append(game.simRound()[0])
print(mode(winners))

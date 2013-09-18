from datetime import datetime, timedelta
import re

MAXWINDOW = timedelta(minutes=10)

def timeOf(stamp):
    times = tuple([int(n) for n in re.findall("[0-9]*", stamp) if n])
    return datetime(*times)

def hourOf(t):
    n = int(t)
    if n == 0: return "midnight"
    elif n < 12: return "%dam" % n
    elif n == 12: return "noon"
    return "%dpm" % (n-12)

def parse(filename):
    curShow = None
    shows = []
    with open(filename) as handle:
        for line in handle:
            if len(line) != 9:
                if curShow:
                    curShow.finish()
                    shows.append(curShow)
                curShow = Show(line)
            else:
                curShow.addTime(line)
    return shows

def findCollisions(shows):
    automation = [s for s in shows if s.isAutomation()]
    humansAll = [s for s in shows if not s.isAutomation()]
    for auto in automation:
        humans = [h for h in humansAll if h.date == auto.date and h.hour == auto.hour]
        for human in humans:
            if any([human.collides(t) for t in auto.times]):
                print human

class Show:
    def __init__(self, header):
        tokens = header.split(',')
        self.date = tokens[0]
        self.hour = "%s-%s" % (hourOf(tokens[1][0:2]), hourOf(tokens[2][0:2]))
        self.show = tokens[3]
        self.dj = tokens[-1].strip()
        self.times = []
        self.windows = []
        self.offset = timedelta()

    def addTime(self, stamp):
        t = timeOf("%s-%s" % (self.date, stamp.strip()))
        # Account for overlapping midnight
        if self.times and t < self.times[-1]:
            self.offset = timedelta(days=1)
        self.times.append(t+self.offset)

    def finish(self):
        if not self.isAutomation():
            for i in range(len(self.times)-1):
                delta = self.times[i+1] - self.times[i]
                if delta < MAXWINDOW:
                    self.windows.append(i)

    def collides(self, time):
        return any([self.times[i] < time < self.times[i+1] for i in self.windows])

    def isAutomation(self):
        return self.dj == "Rick Deckard"

    def __repr__(self):
        if self.isAutomation():
            return "%s %s: Automation with %d songs" % (self.date, self.hour, len(self.times))
        return "%s %s: %s on %s with %d songs and %d valid windows" % (self.date, self.hour, self.dj, self.show, len(self.times), len(self.windows))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            findCollisions(parse(filename))
    else:
        try:
            findCollisions(parse("spin-data.csv"))
        except IOError:
            print "Please specify file."


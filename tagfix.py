import taglib, os

''' a console program for editing music tags
    can be run with full path, relative path or current dir as arg
    supports flac and mp3
'''

__author__      = "andrew donheiser"
__version__ = "1.0"

class trackEdit:

    def __init__(self, mp3Filename):
        self.song = taglib.File(mp3Filename)
        self.tagsLen = len(self.song.tags)

    def saveTrack(self):
        returnVal = self.song.save()
        if returnVal:
            print(returnVal)

    def editTag(self, tagNumber):
        oldVal = None
        choice = None
        _tag = None
        tagMap = dict()
        i = 0

        for t in sorted(self.song.tags.keys()): # generate legend
            tagMap.update({i : t})
            i += 1

        while not choice in ['y', 'n']:         # do edit
            _tag = tagMap[tagNumber]
            oldVal = self.song.tags[_tag]
            self.song.tags[_tag] = [input('enter new value for '+ _tag + ' ~> ')]
            choice = input('save tag? (y/n) ~> ')

        if choice == 'n':
            self.song.tags[_tag] = oldVal   # put the old value back for display purposes
            return 0
        else:
            self.saveTrack()

    def getTagChoice(self):
        choice = None
        tagChoice = -1
        num = [x for x in range(self.tagsLen)]

        while not choice in ['n']:
            choice = None

            while not int(tagChoice) in num:
                tagChoice = input('tag num ~> ')
                try:
                    int(tagChoice)
                except ValueError:
                    tagChoice = -1

            self.editTag(int(tagChoice))
            tagChoice = -1
            choice = input('edit another tag or display current tags (y/n/t) ~> ')
            if choice == 't':
                self.displayTags()
            if choice == 'n':
                return 0

    def isEdit(self):
        choice = None
        while not choice in ['y', 'n']:
            choice = input('modify this track? (y/n) ~> ')
        return True if choice == 'y' else False

    def displayTags(self, tag=None):
        i = 0
        if tag: # user supplied the tag
            print(self.song.tag[tag])
        else:   # no tag specified
            for k,v in sorted(self.song.tags.items()):
                print('{:<0} {:<20} {:<1} {:<20}'.format(str(i), k,'-', v[0] ))
                i += 1
            if self.isEdit():
                self.getTagChoice()
            else: return 0

# feeds files to trackEdit
class tagfixer:

    def go(self):
        choice = None
        ftypes = ('flac', 'mp3')
        while not choice in ['q']:
            choice = input('enter a track or folder or (q to exit) ~> ')
            if choice.endswith(ftypes):
                t = trackEdit(choice) if os.path.exists(choice) else print('nope')
                t.displayTags()
            else:
                if os.path.exists(choice):
                    for f in os.listdir(choice):
                        if f.endswith(ftypes):
                            t = trackEdit(choice + '/' + f)
                            t.displayTags()
                else:
                    choice == 'q' or print('nope')
def usage():
    print('tagfix.py /path/to/(file/dir) or current dir supports flac and mp3\n')

def main():
    t = tagfixer()
    t.go()

if __name__ == '__main__':
    main()
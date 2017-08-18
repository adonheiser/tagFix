import unittest, random, sys, os
import tagfix , uu
import unittest.mock as mock

class tagFixTests(unittest.TestCase):

    # uudecode test mp3 file
    def setUp(self):
        self.mp3File = 'swr.mp3'
        uuFile = 'swr.uu'
        uu.decode(uuFile, self.mp3File)                 # decode the uuendoded test file
        self.assertTrue(os.path.exists(self.mp3File))   # verify it worked
        self.track = tagfix.trackEdit(self.mp3File)

    def tearDown(self):
        del self.track
        os.remove(self.mp3File)

    # check mp3 length
    def testLen(self):
        self.assertEqual(self.track.tagsLen, 13)

    def testRead(self):
        self.assertEqual(self.track.song.tags["ALBUM"], ['Stoner Witch'])

    def testEditSave(self):
        with mock.patch('builtins.input', side_effect=['foo' ,'y']):
            self.track.editTag(0)
        self.assertEqual(self.track.song.tags["ALBUM"], ['foo'])

    def testEditNoSave(self):
        with mock.patch('builtins.input', side_effect=['foo' ,'n']):
            self.track.editTag(0)
        self.assertEqual(self.track.song.tags["ALBUM"], ['Stoner Witch'])

    def testGetTageChoice(self):
        with mock.patch('builtins.input', side_effect=['0' ,'foo', 'y', 'n']):
            self.track.getTagChoice()
        self.assertEqual(self.track.song.tags["ALBUM"], ['foo'])

    def testGetTageChoiceTwice1(self):
        with mock.patch('builtins.input', side_effect=['0', 'foo', 'y', 'y', 0, 'bar', 'y', 'n']):
            self.track.getTagChoice()
        self.assertEqual(self.track.song.tags["ALBUM"], ['bar'])

    def testGetTageChoiceTwice2(self):
        with mock.patch('builtins.input', side_effect=['0', 'foo', 'y', 'y', 0, 'bar', 'n', 'n']):
            self.track.getTagChoice()
        self.assertEqual(self.track.song.tags["ALBUM"], ['foo'])
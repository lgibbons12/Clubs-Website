import unittest
import sheets
info = ('ABC (Athletes Bonding Club) ', 'Caden Elnaggar ', 'The other leaders in this club are Tyler Martin and Cole Haigney. The goals and objectives of this club are to help other athletes in Cannon learn about the different ways to connect with their teammates, whether it is on the field/court, or off of it as friends. Chemistry is a piece of a team that can be very strong when going through a long, rigorous season. It allows the team to stay together, connected, and ultimately continue to strive to achieve the same goals. The club will hold either meetings, or lunches, to talk about different values and morals that athletes can hold themselves and others accountable for in order to build better relationships as friends, and as teammates. As each meeting is held, Cole, Tyler, and I will attempt to bring in different speakers from different levels of varying sports in order to give different perspectives on the subjects we talk about.  ')
class TestMain(unittest.TestCase):

    def test_linking(self):
        self.assertEqual(sheets.main(sheet = 'https://docs.google.com/spreadsheets/d/13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc/edit#gid=391256049', dfy = False, testing_link = True), '13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc')
    
    def test_analyzing(self):
        first_return = sheets.main(sheet = None, dfy = True, testing_link = False)

        self.assertEqual(first_return, info)

if __name__ == '__main__':
    unittest.main()
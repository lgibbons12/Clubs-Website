# Clubs-Website

Okay now we have pretty cool website that can actually show the blog information

Issues right now
- make showing pictures possible
- make websites look pretty
- create form where people can create blog posts

Okay now we just created the clubs showing

and we have a nav bar now\


Okay where we are at
Authentication: firebase kind of set up, need to work on a tutorial to figure that out
Admin: have the spreadsheet refreshing half working, need to add more functionality
SheetsAPI: need to fix token not being saved and get the spreadsheet id and range to generate dynamically
Connection: connect the blog and clubs pages to each other
Javascript and CSS to have the website look good
Add pictures to blog posts?



Notes for Admins:
When looking for a new sheet, click on the first club and change the sheet link to the link they want
then select that club and run new club info

From then on, they can just click the first one and new club info, and they only have to change it when they want to change the spreadsheet link



CVurrently working on dynamically generating the range

here is the error right now
======================================================================
ERROR: test_linking (__main__.TestMain.test_linking)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\lgibbons\Documents\cool\Clubs-Website\google_sheets\test_sheets.py", line 9, in test_linking
    self.assertEqual(sheets.main(sheet = sheety, dfy = False, testing_link = True), '13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc')
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\lgibbons\Documents\cool\Clubs-Website\google_sheets\sheets.py", line 100, in main
    df = pd.DataFrame(data = values[1:], columns=values)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\lgibbons\Documents\cool\venv\Lib\site-packages\pandas\core\frame.py", line 808, in __init__
    columns = ensure_index(columns)
              ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\lgibbons\Documents\cool\venv\Lib\site-packages\pandas\core\indexes\base.py", line 7564, in ensure_index
    return MultiIndex.from_arrays(index_like)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\lgibbons\Documents\cool\venv\Lib\site-packages\pandas\core\indexes\multi.py", 
line 529, in from_arrays
    raise ValueError("all arrays must be same length")
ValueError: all arrays must be same length

----------------------------------------------------------------------
Ran 2 tests in 0.955s

FAILED (errors=2)
i think it has something to do with some of the rows and columns being blank
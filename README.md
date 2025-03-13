# This is a bot I am creating to keep track of square meters of stone slabs that are produced at a stone cutting factory in my city.

---

## The goal:

+ __Eliminate waste of paper to save the forests.__
+ __Simplify accounting by automatically multiplying square meters from the input slab sizes.__
+ __Make it possible for each worker to pass the data of his finished product to a common database in any way convenient. He should be able to use either his smartphone or a PC and should be able to interact with either the telegram bot or the web app to pass the data.__
+ __Then at the end of the day the factory bookkeeper should be able to see a table filled by all the workers who were on the shift that day. With all square meters already calculated out. Then all he will need to do is take the data of each separate worker and issue hit the days wages depending on the price per square meter.__
 
## Future goals:

+ __Expand the simple bot into a bigger app written with Angular framework to allow more than one worker to use it.__
+ __Save all input data on a server and make an api with charts and schedules so a bookkeeper can open it, inspect how
  many square meters each worker produced per month and issue a salary accordingly.__

___

## How to run the project

1) __Fork and clone the repo to the local machine using this command;__

> git clone https://github.com/mylcevaleksandr/Stone_Cutter_Auditor.git .

2) __Open terminal in project directory root and run;__

> python -m venv venv

3) __Install project dependencies;__

> pip install -r requirements.txt

4) __Create .env file and add the following code to it;__

> export BOT_TOKEN="your bot token"
> > Hint; You will need a valid bot token. Create your own telegram bot using [@BotFather](https://t.me/BotFather) and
> > use its token for development and testing. Or contact me [@Aleksandr_Website_Dev](https://t.me/Aleksandr_Website_Dev)
> > and I will send you the token of my bot.

5) __Run bot.py to activate the telegram bot.__
6) __Navigate to the  [@Stone_Cutter_Accounting_bot](https://t.me/Stone_Cutter_Accounting_bot) and start interacting.__

___ 

## Current Tasks

1) __Define a function to prompt the user what saw number he is currently working on__ _in a range from one to six_

> Example: Saw number one

2) __After the saw is selected. Prompt for the block number and cubic meters__

> Example: Block number: 135, 2.5 m3.

3) __Allow the user to enter new slab numbers and sizes in millimeters__

> Example: Slab number = 135-1. Length = 1200mm, width = 550mm.

4) __Show the user the square meters of the current slab__

> Example: Slab# 135-1, 0.66 m2.

5) __Give an option to see all slabs produced on the current saw in the current work shift__

> Example: Monday, November 22, Saw# 1, Slabs: 135-1, 0.66m2; 135-2, 0.66m2; 135-3, 1.80m2. __Total m2 = 3.12.__

6) __Give an option to make changes to the produced slabs, their sizes and names.__
7) __Give an option to hand over part of a block to the next shift__

> Example: New block number: 135/1, 1.25 m3

8) __Allow user to switch between all six saw installations__
9) __Allow user to see all square meters produced on six saws__

___

# Contributions Welcome!




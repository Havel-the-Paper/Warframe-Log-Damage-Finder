Damage in warframe is pretty straightforward provided you are dealing less than 2,147,483,647 damage in one instance. If you hit higher than this it wraps into a negative, and starts climbing back up to 0 before looping again. This means 3,147,483,647 damage will likely display in game as something close to -1,147,483,647. 
Players at endgame can hit so high that the displayed numbers can be rather meaningless at times, but there is a log that keeps track of the actual numbers.
Warframe outputs a log on pc that has an error when you do too much damage. It shows you what the in-game number would have showed, and then the actual damage dealt. So I wrote a python script that goes through the full log, finds the biggest damage number, then tells you where in the log to find it so you can review what dealt the damage and who took it.
Below is an example of what the log might find, showing ~42 billion damage dealt to a demolisher devourer with the Opticor Vandal:
![Opticor 42 Billion](https://github.com/user-attachments/assets/db422db5-96d3-4436-981a-c3da7e66e8f1)
Now here is the result of this tool:
![image-14](https://github.com/user-attachments/assets/956369a6-b698-488f-aab0-2df0a32f4c18)

# AI disclaimer

Claude.ai version 3.7 Sonnet in extended thinking mode is better than me. What I mean by that is that, by now, Claude is more capable,
more effective and more precise when it comes to digital routine tasks, such as coding and writing, than I could ever be. 
Where in the recent past LLMs sometimes struggled with seemingly basic reasoning and misinterpreting human problems, this is no more.

---

## Setup

This project has been created in complete cooperation with this model; **Anthropics Claude.ai 3.7 Sonnet in Extended thinking mode**. 
<br> I tasked Claude to create a full workshop for me with the goal of completing this game, Cell Wars, to which I developed the idea throughout class. 
The initial prompt that I used to start the workshop, which I have outlined in a brief descriptive document is also in this folder under the name: **CellWars_Prompt_GameDescription**

Claude's summary of the task went like this:

>Based on the document you've uploaded, I understand that I need to:
>
>1. Create a two-week workshop to guide you through programming "Cell Wars" - a two-player, turn-based game using Python and Pygame
>2. Break down the workshop into daily tasks/lessons that are detailed and easy to understand for someone with minimal programming knowledge
>3. Create a scoring system to track your progress as you complete tasks
>4. Structure the workshop so you'll have a minimal working prototype by the end of two weeks that includes:
   >- The core game mechanics (cellular automata-based moves, grid battlefield, turn-based gameplay)
   >- Networking capabilities for two-player functionality
   >- GitHub integration (repo creation and uploading via Mac terminal)
>5. Include optional bonus tasks for enhancements like improved graphics or sound

This summary describes how we worked together. The whole workshop did work out extremely well. 

---

## Development

Claude would break down the tasks into reasonable chunks and walk me through the code creation step-by-step. 
He would pre-create code to give me orientation points but would also guide me through writing, implementing and updating my own pieces of code.
If I had trouble understanding parts of his code or had ideas on how to improve it, we would discuss those ideas and implement changes if we 
came to the conclusion that it would make sense. As a general rule of thumb, I never used copy/paste on any of his code but made it a point to type everything out by hand which helped me to understand 
processes line by line.
<br>He also taught me how to set up my GitHub Repo and how to push changes through the terminal, which I know use daily to keep everything updated.

Generally, Claude acted as my personal teacher who had developed a specialized workshop just for me and my project and who understood what I wanted to learn and achieve with this.

Here is an examples on how we talked about code pieces: 
<br>The context is the creation of the cell grid and the way how to leave space between each cell:

### **Question:**
> I created the grid.py script and everything works as expected, however I got a question: why do you use:
```python
pygame.draw.rect(surface, (50, 50, 50), rect, 1)  # Grid lines
```
>Instead of creating the grid in a way to leave a 1px space around each cell?

### **Answer:**
>**Approach 1: Drawing borders (what we're using)**
```python
pygame.draw.rect(surface, self.colors[self.cells[y][x]], rect)
pygame.draw.rect(surface, (50, 50, 50), rect, 1)  # Grid lines
```
>**Approach 2: Leaving spacing between cells**
 ```python
rect = pygame.Rect(
    x * (self.cell_size + 1) + 1,  # Add 1px spacing and 1px offset
    y * (self.cell_size + 1) + 1, 
    self.cell_size, 
    self.cell_size
)
pygame.draw.rect(surface, self.colors[self.cells[y][x]], rect)
```

>Why We Chose Approach 1:
Simplicity of coordinate mapping - With the current approach, there's a direct 1:1 mapping between grid coordinates and pixel positions (multiplied by cell size). This makes mouse interaction much easier to calculate.

I immediately understood the thought process behind that because I knew how annoying it can be to map offset to coordinates (been there, done that)

---
<br>
Sometimes Claude would make structural mistakes, which I always tried to point out:

### **Question:**
> We also need to find a way to distribute the Player Color Variable throughout our scripts, because now we define the player colors in two places: The Grid (to define the grid color that players add) and int the game_manager.

### **Answer:**
>You've identified another excellent design issue! Having player colors defined in multiple places is a recipe for inconsistency. Let's fix that with a more cohesive approach.

---

<br>
I sometimes had to ask Claude to make code more easily approachable, at the cost of length or precision, for me to be able to fully understand what it is doing.

### **Question:**
> This line seems to be a bit overengineered, please rewrite it to be easier understandable:
 ```python
self.current_player_index = (self.current_player_index + 1) % len(self.players)
```
### **Answer:**
> For a strictly two-player game, that line is indeed more complex than necessary.
> The line could be simplified to:
 ```python
self.current_player_index = 1 - self.current_player_index
```
---
<br>
Sometimes I asked Claude to explain some concepts to me which are relevant to coding:

### **Question:**
 ```python
move_name = f"Move {(i % 3) + 1}"
```

>I understand what modulo does, but why does 2 % 3 equals 2? How does modulo work if the result is lower than 1?

### **Answer:**
>That's a great question about modulo! The modulo operation (%) returns the remainder after division, and it works even when the first number is smaller than the second.
Here's how modulo works in all cases:
If we have a % b:
> 
>We're calculating the remainder when a is divided by b
When a is smaller than b, a cannot be divided by b at all (the quotient is 0), so the remainder is just a itself
> 
>So for 2 % 3:
> 
> 2 ÷ 3 = 0 with a remainder of 2 
> 
> Therefore, 2 % 3 = 2

<br>
Overall, we had hundreds of these interactions. If you are interested in the process or to look at more interactions please let me know and I will be fully transparent with the whole process.

---
## Difficulties
There have been a few difficulties throughout the development process:

<br>Claude surprisingly had a lot of trouble keeping track of my scores. He was supposed to develop a scoring system to give me points for tasks, which initially worked out well, but which gradually degraded. 
He would sometimes give me points for asking a simple question instead of solving a task and oftentimes simply forget to score me. Eventually I ditched the whole system and stopped reminding him of my scores. I am however fully confident that with more carefull prompting this could have worked out better.

Claude had a tendency to be too fast with generating code even if I asked him be slow and 
guide me step-by-step. I sometimes had to stop his response creation because it would eagerly 
create a bunch of new scripts which he considered useful at the moment. 
After a while I learned how to write more specific prompts to avoid this behaviour, and he learned to be slower and more meticulous.

There are parts of the code which I am still having trouble to understand, mostly in the networking process. Claude did his best to explain it to me, but I am just not advanced enough in my understanding of some of the structures to be able to full grasp its meaning.
I am however fully confident that this is not a problem with the method of the AI workshop and that I would have the same (if not more so) difficulties if I had worked with a tutorial on network programming.


---
## Conclusion

Generally, the process of working together with Claude went unbelievably well. His code was always very clear and almost never had any actual bugs (besides being sometimes redundant). 
What impressed me most was his ability to grasp what I wanted of him even if my descriptions sometimes where pretty vague. I never (!) felt completely misunderstood 
<br>I feel like I have learned an enormous amount about coding in a short time span, and I am now under the impression that I could cooperate with Claude to create any kind of project; be it games, apps or websites.

**However**, I do want to acknowledge that this way of working *does not* consolidate knowledge in the way that classical learning would. 
I feel confident about my code and I could explain how it works, but I would not be able to rebuild this project now without the help of Claude. Not all the concepts and syntax will stay in my head and I would have trouble coming back to the code in six months and still fully understand it.

<br>I do feel though, that this way of cooperative work with AI is the future of digital work and that my approach taught be very valuable knowledge about that process. I am fully confident that I will continue
on the path of AI cooperation successfully and that this was just the first step for me.



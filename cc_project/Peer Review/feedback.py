def peer_review_guidelines():
    """
    Peer Review: Blackjack Card Counting Simulator (Darrel & Lennard) & Checked by Elina
    Peer Review Guidelines:
    -----------------------
    The groups will pair up. They will each descri`be their project to the other,
    noting any bugs or difficulties. Each group will write and submit a brief reflection
    (approximately 500 words) describing the other group's projects. Consider the following questions
    in your reflection:

      What is the other group’s project supposed to do? How can this be made
        more clean?

        The project is designed to simulate and teach blackjack card counting using the Hi-Lo system. One part of the code is an 
        interactive tutorial where users input the running count as cards are revealed, while the other part is an automated simulation 
        that deals cards and calculates the true count dynamically. The code is fairly structured, but it could be made cleaner by reducing 
        redundancy, improving function documentation, and separating concerns (e.g., placing the plotting logic in a separate module).

        Are there any bugs? How can you be sure?

        I didn’t see any big mistakes, but to be sure, the code should be tested with different situations, like an empty deck or wrong 
        user input. Writing small test programs to check if the counting works right would help.

        Is it clear what the project does and how to run it, based only on the
        github page?

        Since there’s no GitHub page provided, I’m not sure if the instructions are clear. If there aren’t any, adding a 
        README file with setup steps, examples, and a list of things you need (like Matplotlib) would make it easier to use. 
        Additionally, more comments in the code would allow for more deciphering on what the code does.


        Do you have any suggestions for how to improve the structure of the other
        group’s code, or their workflow?

        The code could be organized better by putting different parts into separate files, like one for handling the deck and another for 
        counting cards. Making the counting system its own class could also help keep things neat.

        Did you notice the other group doing anything clever that you will adopt?

        The accuracy tracking feature is a smart idea because it shows how well someone is counting cards over time. This could be useful in 
        other projects to give feedback while learning. Specifically implementing in tracking my user’s performance in rounds in my Block Blast
        program


    Note:
      This "Peer Review" step is not intended to be an evaluation.
      You are not expected to grade each other's projects.
      The reasons for this step are to:
         - Get useful advice from other groups.
         - Gain perspective and confidence about whether you are on the right track.
         - See your own project from an outside viewpoint to identify unclear goals and achievements.
    """
    print(peer_review_guidelines.__doc__)

if __name__ == '__main__':
    peer_review_guidelines()

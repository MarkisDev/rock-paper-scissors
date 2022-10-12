import random
from github import Github


class RPS:
    def __init__(self, token, issueNumber, repo):
        self.token = token
        self.repo = Github(token).get_repo(repo)
        self.issue = self.repo.get_issue(issueNumber)
        self.moves = ['rock', 'paper', 'scissor']
        self.filePath = 'README.md'

    def fetchFileFromRepo(self, filepath):
        return self.repo.get_contents(filepath)

    def writeToRepo(self, filepath, message, content, sha):
        self.repo.update_file(filepath, message, content, sha)

    def addComment(self, message):
        self.issue.create_comment(message)

    def computerMove(self):
        self.computerMove = random.choice(self.moves)

    def didUserWin(self, userMove):
        if ((userMove == 'rock' and self.computerMove == 'scissor') or (userMove == 'scissor' and self.computerMove == 'paper') or (userMove == 'paper' and self.computerMove == 'rock')):
            return True
        elif (userMove == self.computerMove()):
            return None
        else:
            return False

    def genFileData(self, userName, result):
        outer = div()
        with outer:
            h1("Rock Paper Scissors Game!")
            p("Click on one of the below actions to play your move:")
            h3(":first: :hand: :scissors:")
            if result == True:
                h4(f"Previous winner was @{userName} :tada:!")
            elif result == False:
                h4(f"Previous winner was computer :robot:!")
            else:
                h4(f"Previous game was a draw :eyes:!")
        return outer.render()

import random
from github import Github
from dominate.tags import *


class RPS:
    def __init__(self, token, issueNumber, repo):
        self.token = token
        self.repo = Github(token).get_repo(repo)
        self.issue = self.repo.get_issue(issueNumber)
        self.moves = ['rock', 'paper', 'scissor']
        self.filePath = 'README.md'

    def playMove(self):
        fileData = self.fetchFileFromRepo(self.filePath)
        userName = self.issue.user.login
        move = self.issue.title.lower().split('|')
        if (len(move) > 1) and move[1] in self.moves:
            move = move[1]
            self.computerMove = self.computerMove()
            if (move == 'rock'):
                action = ":fist:"
            elif (move == 'paper'):
                action = ":hand:"
            else:
                action = ":scissors:"
            if move in self.moves:
                result = self.didUserWin(move)
                newFileData = self.genFileData(userName, result)
                if result == True:
                    self.addComment('Congratulations! You won! :tada:')
                    self.writeToRepo(self.filePath, f"@{userName} won with {action}", newFileData, fileData.sha)
                elif result == None:
                    self.addComment('Oops! This was a draw! :eyes:')
                    self.writeToRepo(self.filePath, f"@{userName} played {action}", newFileData, fileData.sha)
                elif result == False:
                    self.addComment(
                        f'Uh-Oh! You lost! :eyes:\n Computer played {self.computerMove}')
                    self.writeToRepo(self.filePath, f":robot: won with {action}", newFileData, fileData.sha)
        else:
            self.addComment('You played an invalid move! :eyes:')
        self.issue.edit(state="closed")

    def fetchFileFromRepo(self, filepath):
        return self.repo.get_contents(filepath)

    def writeToRepo(self, filepath, message, content, sha):
        self.repo.update_file(filepath, message, content, sha)

    def addComment(self, message):
        self.issue.create_comment(message)

    def computerMove(self):
        return random.choice(self.moves)

    def didUserWin(self, userMove):
        if ((userMove == 'rock' and self.computerMove == 'scissor') or (userMove == 'scissor' and self.computerMove == 'paper') or (userMove == 'paper' and self.computerMove == 'rock')):
            return True
        elif (userMove == self.computerMove):
            return None
        else:
            return False

    def genFileData(self, userName, result):
        outer = div()
        repo = self.repo.full_name
        with outer:
            h1("Rock Paper Scissors Game!")
            p("Click on one of the below actions to play your move:")
            h3(a(":fist:", href=f'https://github.com/{repo}/issues/new?title=rps|rock'), a(":hand:", href=f'https://github.com/{repo}/issues/new?title=rps|paper'), a(":scissors:", href=f'https://github.com/{repo}/issues/new?title=rps|scissor'))
            if result == True:
                h4(f"Previous winner was @{userName} :tada:")
            elif result == False:
                h4(f"Previous winner was computer :robot:")
            else:
                h4(f"Previous game was a draw :eyes:")
        return outer.render()

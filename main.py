import random
from github import Github


class RPS:
    def __init__(self, token, issueNumber, repo):
        self.token = token
        self.repo = Github(token).get_repo(repo)
        self.issue = self.repo.get_issue(issueNumber)
        self.moves = ['rock', 'paper', 'scissor']
        self.fileName = 'README.md'

    def fetchFileFromRepo(self, filepath):
        return self.repo.get_contents(filepath)

    def writeToRepo(self, filepath, message, content, sha):
        self.repo.update_file(filepath, message, content, sha)

    def addComment(self, message):
        self.issue.create_comment(message)

    def computerMove(self):
        self.computerMove = random.choice(self.moves)

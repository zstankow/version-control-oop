"""
Contains 2 classes for Version control of single information pieces, like numbers:
- "Commit" with information about a single commit
- "Repo" with information about commits of numbers
"""


class Commit:
    nums_all = {}

    def __init__(self, message, nums_added_changed=None, prev_commit=None):
        """
        Initiate a single Commit with information about commit message, what numbers were changed
            and snapshot of all numbers.
            Each number versioned has a "name" and a "value".
            Values can be updated for existing number, but a number can not be deleted.

        :param message: commit message that explains the commit
        :param nums_added_changed: dictionary of {number_name: number_value}
            of numbers that were added or changed in the current commit.
            If not given (None) - assumed that no numbers were changed
                (valid only for initial commit of creation of repo)
        :param prev_commit: Instance of Commit class of the previous commit.
            If not given (None) - assumed that this is the first commit of the repository
        """
        self.message = message
        self.nums_added_changed = nums_added_changed if nums_added_changed else {}
        self.prev_commit = prev_commit if prev_commit else None
        self.nums_all = self.update_nums_all(nums_added_changed) if nums_added_changed else self.nums_all

    def __str__(self):
        """
        Returns string representation of a Commit
        Example of a string: 'Commit message: "msg3", 2 numbers added/changed, 3 total numbers'

        :return: String representation of a Commit (see example above)
        """
        return (f'Commit message: "{self.message}", {len(self.nums_added_changed)} numbers added/changed, '
                f'{len(self.nums_all)} total numbers')

    def update_nums_all(self, nums):
        nums_all = self.prev_commit.nums_all.copy()
        nums_all.update(nums)
        return nums_all

    def __getitem__(self, key):
        return self.nums_all[key]

class Repo(Commit):

    def __init__(self, repo_name, initial_commit_msg):
        initial_repo = Commit(initial_commit_msg)
        super().__init__(initial_repo.message, initial_repo.nums_added_changed, initial_repo.prev_commit)
        """
        Initialize an empty repository with an "empty" commit (no numbers)
        :param repo_name: name of repository to initialize
        :param initial_commit_msg: commit message of the initial commit
        """
        self.repo_name = repo_name
        self.staged = {}
        self.commits = [initial_repo]

    def stage(self, num_name, num_value):
        """
        Stage a number with the given value
        :param num_name: name of number to stage
        :param num_value: value of number to stage
        """
        self.staged[num_name] = num_value

    def commit(self, message):
        """
        Commit staged numbers
        :param message: commit message of the commit
        """
        new_commit = Commit(message, self.staged, self)
        self.nums_all = new_commit.nums_all
        self.staged = {}
        self.commits.append(new_commit)

    def __str__(self):
        return f'Repo "{self.repo_name}", {len(self.commits)} commits, {len(self.staged)} numbers staged'

from PhraseDatabases import EightBall, Excuses, Commands
from RandomFun import Straws
from collections import defaultdict
from pymarkovchain import MarkovChain


def _db_factory():
    return defaultdict(_one_dict)


def _one():
    return 1.0


def _one_dict():
    return defaultdict(_one)


class ResponseGenerator:

    def __init__(self):
        self.eightball = EightBall()
        self.excuses = Excuses()
        self.commands = Commands()
        self.straws = Straws("/", "=", "/")
        self.chain = MarkovChain("./markovdb")
        self.chain.db = _db_factory()
        with open("markovsource", "r") as markov_file:
            self.chain.generateDatabase(markov_file.readline())

    def generate_response(self, body):
        # Tokenize body
        body_tokens = body.lower().split(" ")
        # Important commands can only be run if line is started with the word
        command = body_tokens[0]

        if command == '!create':
            new_command = body_tokens[1]
            response_index = body.find(new_command) + len(new_command) + 1
            response = body[response_index:]
            self.commands.set(new_command, response)

            return "Command !{0} created.".format(new_command)

        elif command == "!list":
            string = "!create !delete !reload !excuse !8ball !straws !image "
            for command_ in self.commands.list():
                string += "!{0} ".format(command_)

            return string

        elif command == "!delete":
            cleaned_command = body_tokens[1].lower()
            success = self.commands.delete(cleaned_command)

            if success:
                return "Command !{0} deleted.".format(cleaned_command)
            else:
                return "Command !{0} does not exist.".format(cleaned_command)

        elif command == "!reload":
            with open("markovsource", "r") as markov_file:
                self.chain.generateDatabase(markov_file.readline())

            return "Successfully reloaded my word database"

        # Not a system command, continue attempting to parse
        else:
            for token in body_tokens:
                if token == "!fortune":
                    # TODO
                    pass
                elif token == "!excuse":
                    return self.excuses.get()

                elif token == "!8ball":
                    return self.eightball.get()

                elif token == "!straws":
                    return self.straws.get()

                elif token == "!image":
                    return "/get " + self.chain.generateString()

                elif token == "tase":
                    return self.chain.generateString()

                elif len(token) > 0 and token[0] == "!":
                    return self.commands.get(token[1:])

                # we have a sentence to listen to, arbitrary length requirement
                elif len(body) > 10:
                    string_to_write = body + "."
                    if body[len(body) - 1] == ".":
                        string_to_write = body

                    with open("markovsource", "a") as markov_file:
                        markov_file.write(string_to_write)

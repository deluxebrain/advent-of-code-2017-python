"""Solutions to day 4 parts 1 and 2."""

def load(day):
    """Open specified days input file."""
    filename = 'input_{}.txt'.format(str(day).zfill(2))
    return open(filename).read()

def is_passphrase_valid(passphrase):
    """Checks if passphrase is valid by checking for
    any repeated words."""
    valid = True
    words = set()
    for word in passphrase.split():
        if word not in words:
            words.add(word)
        else:
            valid = False
            break
    return valid

# Part 1 test cases
assert is_passphrase_valid("aa bb cc dd ee")
assert not is_passphrase_valid("aa bb cc dd aa")
assert is_passphrase_valid("aa bb cc dd aaa")

def are_passphrases_valid(passphrases, strategy):
    """Parse file of passphrases and return count of those
    that are valid."""
    valid_passphrases = [passphrase for passphrase
                         in passphrases.splitlines()
                         if strategy(passphrase)]
    return len(valid_passphrases)

# Solution to part 1
print("Solution to part 1: {}". format(are_passphrases_valid(
    load(4),
    is_passphrase_valid)))

def day_2_strategy(passphrase):
    """Return if passphrase is valid is no repeat words
    and no anagrams."""
    valid = True
    words = set()

    for word in passphrase.split():
        sorted_word = ''.join(sorted(word))
        if sorted_word not in words:
            words.add(sorted_word)
        else:
            valid = False
            break

    return valid

# Part 2 test cases
assert day_2_strategy("abcde fghij")
assert not day_2_strategy("abcde xyz ecdab")
assert day_2_strategy("a ab abc abd abf abj")
assert day_2_strategy("iiii oiii ooii oooi oooo")
assert not day_2_strategy("oiii ioii iioi iiio")

# Solution to part 2
print("Solution to part 2: {}".format(
    are_passphrases_valid(load(4), day_2_strategy)
))

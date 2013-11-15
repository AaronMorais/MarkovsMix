import random

class MarkovModel:

    def learn_ngram_distribution(self, items, n):
        """ This function takes an array of items, applies a markov model to
        them where states are n grams of the elements in items
        """
        if n > len(items):
            print "that's wrong"
            return
        self.transitions = dict()
        self.n = n

        # look at the first ngram before the loop, to populate prev_ngram
        prev_ngram = tuple(items[0:n])
        self.transitions[prev_ngram] = dict()
        pos = 1

        while pos + n < len(items):
            # update current ngram, and update transitions for prev_ngram
            curr_ngram = tuple(items[pos:pos+n])
            if curr_ngram not in self.transitions[prev_ngram]:
                self.transitions[prev_ngram][curr_ngram] = 1
            else:
                self.transitions[prev_ngram][curr_ngram] += 1

            if curr_ngram not in self.transitions:
                self.transitions[curr_ngram] = dict()
            pos += 1
            prev_ngram = curr_ngram

    def generate_a_bunch_of_text(self, ngrams_to_use=50):
        ngram = self.generate_initial_ngram()
        output = []
        for c in ngram:
            output.append(c)
        ngrams_used = 1
        while ngrams_used < ngrams_to_use:
            ngram = self.generate_next_ngram(ngram)
            output.append(ngram[-1])
            ngrams_used += 1
        return output

    def generate_initial_ngram(self):
        total_ngrams = 0
        for ngram in self.transitions:
            total_ngrams += self._frequency_of_ngram(self.transitions[ngram])
        chosen_ngram_pos = random.randint(1, total_ngrams)
        curr_range = 0
        for ngram in self.transitions:
            curr_range += self._frequency_of_ngram(self.transitions[ngram])
            if chosen_ngram_pos <= curr_range:
                return ngram
        print "this shouldn't have happened"
        return None

    def generate_next_ngram(self, prev_ngram):
        if prev_ngram not in self.transitions:
            print "what are you doing"
            return
        num_range = self._frequency_of_ngram(self.transitions[prev_ngram])
        if num_range == 0:
            return self.generate_initial_ngram()
        chosen_ngram_pos = random.randint(1, num_range)
        curr_range = 0
        for ngram, freq in self.transitions[prev_ngram].iteritems():
            curr_range += freq
            if chosen_ngram_pos <= curr_range:
                return ngram
        print "uh oh I should never be executed"
        return None

    def _frequency_of_ngram(self, ngram_map):
        """ takes a dictionary from ngrams to counts and returns the sums of the counts"""
        return sum(ngram_map.values())

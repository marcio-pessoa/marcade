
import unittest

# Mocking the M2048 class to test logic without pygame
class MockM2048:
    def __init__(self):
        self.grid_size = 4
        self.score = 0
        self.grid = [[0] * 4 for _ in range(4)]

    def _merge(self, line):
        # Copy of the logic we intend to implement in m2048.py
        # Returns (new_line, moves)
        # moves is a list of dicts: {'from': index, 'to': index, 'value': val, 'merged': bool}

        non_zero = []
        for i, val in enumerate(line):
            if val != 0:
                non_zero.append({'val': val, 'orig_index': i})

        merged_line = []
        moves = []
        skip = False

        target_index = 0
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue

            current = non_zero[i]

            if i + 1 < len(non_zero) and current['val'] == non_zero[i + 1]['val']:
                # Merge
                next_tile = non_zero[i+1]
                new_val = current['val'] * 2
                self.score += new_val

                moves.append({'from': current['orig_index'], 'to': target_index, 'value': current['val'], 'merged': False}) # First tile moves to target
                moves.append({'from': next_tile['orig_index'], 'to': target_index, 'value': next_tile['val'], 'merged': True}) # Second tile moves to target and merges

                merged_line.append(new_val)
                skip = True
            else:
                # No merge
                moves.append({'from': current['orig_index'], 'to': target_index, 'value': current['val'], 'merged': False})
                merged_line.append(current['val'])

            target_index += 1

        # Pad with zeros
        final_line = merged_line + [0] * (len(line) - len(merged_line))

        return final_line, moves

class Test2048Logic(unittest.TestCase):
    def setUp(self):
        self.game = MockM2048()

    def test_simple_move(self):
        line = [0, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [2, 0, 0, 0])
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0]['from'], 1)
        self.assertEqual(moves[0]['to'], 0)

    def test_merge(self):
        line = [2, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 0, 0, 0])
        self.assertEqual(len(moves), 2)
        # Both move to 0
        self.assertEqual(moves[0]['to'], 0)
        self.assertEqual(moves[1]['to'], 0)
        self.assertTrue(moves[1]['merged'])

    def test_move_and_merge(self):
        line = [2, 0, 2, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 0, 0, 0])
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0]['from'], 0)
        self.assertEqual(moves[0]['to'], 0)
        self.assertEqual(moves[1]['from'], 2)
        self.assertEqual(moves[1]['to'], 0)

    def test_no_move(self):
        line = [4, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 2, 0, 0])
        # Even if they don't change visual position, our logic might generate "moves" from i to i.
        # It's okay if it does, or doesn't, as long as we handle it.
        # Let's see what our logic does.
        self.assertEqual(moves[0]['from'], 0)
        self.assertEqual(moves[0]['to'], 0)
        self.assertEqual(moves[1]['from'], 1)
        self.assertEqual(moves[1]['to'], 1)

if __name__ == '__main__':
    unittest.main()

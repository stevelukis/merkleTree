class MerkleTree:

    def __init__(self) -> None:
        self.levels = []

    class Node:
        def __init__(self, value) -> None:
            self.left_child = None
            self.right_child = None
            self.value = value
            self.hash = self.get_hash(value)

        @staticmethod
        def get_hash(value):
            return hash(value)

    def build_tree(self, data: list):
        nodes = [self.Node(value) for value in data]
        self.levels.append(nodes)

        while len(nodes) != 1:
            upper_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1]

                parent = self.Node(left.hash + right.hash)
                parent.left_child = left
                parent.right_child = right
                upper_level.append(parent)
            nodes = upper_level
            self.levels.insert(0, nodes)

    def get_root(self):
        return self.levels[0][0].hash

    def get_proof(self, index):
        proof = []
        for i in range(len(self.levels) - 1, 0, -1):
            level = self.levels[i]
            is_right = index % 2
            if is_right:
                sibling_index = index - 1
                sibling_pos = 0
            else:
                sibling_index = index + 1
                sibling_pos = 1
            proof.append({sibling_pos: level[sibling_index].hash})
            index = int(index / 2.)
        return proof

    def verify(self, proof, root, leaf):
        current_hash = leaf
        for p in proof:
            is_right, sibling_hash = next(iter(p.items()))
            if is_right:
                current_hash = self.Node.get_hash(current_hash + sibling_hash)
            else:
                current_hash = self.Node.get_hash(sibling_hash + current_hash)
        return current_hash == root


data = [
    "coke", "firework", "night", "winter"
]
tree = MerkleTree()
tree.build_tree(data)
proof = tree.get_proof(0)
root = tree.get_root()
is_correct = tree.verify(proof, root, hash(data[0]))
print("Done!")

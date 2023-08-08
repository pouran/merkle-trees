import unittest
import merkle_tree

# tree with 4 leaves: hello1, hello2, hello3, hello4
# example generated using https://xorbin.com/tools/sha256-hash-calculator?utm_content=cmp-true
# 91e9240f415223982edc345532630710e94a7f52cd5f48f5ee1afc555078f0ab is hello1
# 87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4 is hello2
# 47ea70cf08872bdb4afad3432b01d963ac7d165f6b575cd72ef47498f4459a90 is hello3
# e361a57a7406adee653f1dcff660d84f0ca302907747af2a387f67821acfce33 is hello4
# hello1 & hello2: e84e52a730f444505656e5fd583982162a09f45cd8ae50661b4ab6717d135e86
# hello3 & hello4: a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9
# root: 1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834
# proof for hello1 is hello2, hello3 & hello4
# proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
# root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'

class TestMerkleTree(unittest.TestCase):
    
    def test_hash(self):
        expected_hash = '91e9240f415223982edc345532630710e94a7f52cd5f48f5ee1afc555078f0ab'
        self.assertEqual(merkle_tree.hash('hello1'), expected_hash)
    
    def test_parent_creation(self):
        node1 = merkle_tree.Node(merkle_tree.hash('hello1'))
        node2 = merkle_tree.Node(merkle_tree.hash('hello2'))
        expected_parent_value = 'e84e52a730f444505656e5fd583982162a09f45cd8ae50661b4ab6717d135e86'
        parent = merkle_tree.create_parent(node1, node2)
        self.assertEqual(parent.value, expected_parent_value)
        self.assertEqual(parent.left, node1)
        self.assertEqual(parent.right, node2)
        self.assertEqual(node1.parent, parent)
        self.assertEqual(node2.parent, parent)
    
    def test_constructor_with_power_of_2(self):
        values = ['hello1', 'hello2', 'hello3', 'hello4']
        expected_root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        m_t = merkle_tree.MerkleTree(values)
        self.assertEqual(m_t.root.value, expected_root_value)
    
    def test_constructor_with_no_power_of_two(self):
        # dummy is b5a2c96250612366ea272ffac6d9744aaf4b45aacd96aa7cfcb931ee3b558259
        # hello3 & dummy is ba7033dad6fb92fbf9ac9521165c5eff771c0bbf34b1a811d2ce98002e98a5d4
        # expected root is f357c285de34fd9093f85375744796e809f587195b7fe23c428ec09dba08ac95
        values = ['hello1', 'hello2', 'hello3']
        expected_root_value = 'f357c285de34fd9093f85375744796e809f587195b7fe23c428ec09dba08ac95'
        m_t = merkle_tree.MerkleTree(values)
        self.assertEqual(m_t.root.value, expected_root_value)

    def test_constructor_with_1_elem(self):
        values = ['hello1']
        expected_root_value = '91e9240f415223982edc345532630710e94a7f52cd5f48f5ee1afc555078f0ab'
        m_t = merkle_tree.MerkleTree(values)
        self.assertEqual(m_t.root.value, expected_root_value)
    
    def test_proof_verification_correct_proof_1(self):
        # this is proof for hello1
        value = 'hello1'
        correct_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 0, correct_proof, root_value)
        self.assertTrue(result)

    def test_proof_verification_correct_proof_2(self):
        # this is proof for hello2
        value = 'hello2'
        correct_proof = ['91e9240f415223982edc345532630710e94a7f52cd5f48f5ee1afc555078f0ab', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 1, correct_proof, root_value)
        self.assertTrue(result)

    def test_proof_verification_correct_proof_3(self):
        # this is proof for hello3
        value = 'hello3'
        correct_proof = ['e361a57a7406adee653f1dcff660d84f0ca302907747af2a387f67821acfce33', 'e84e52a730f444505656e5fd583982162a09f45cd8ae50661b4ab6717d135e86']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 2, correct_proof, root_value)
        self.assertTrue(result)

    def test_proof_verification_correct_proof_4(self):
        # this is proof for hello4
        value = 'hello4'
        correct_proof = ['47ea70cf08872bdb4afad3432b01d963ac7d165f6b575cd72ef47498f4459a90','e84e52a730f444505656e5fd583982162a09f45cd8ae50661b4ab6717d135e86']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 3, correct_proof, root_value)
        self.assertTrue(result)

    def test_proof_verification_index_out_of_bounds(self):
        # this is proof for hello1
        value = 'hello1'
        correct_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 4, correct_proof, root_value)
        self.assertFalse(result)

    def test_proof_verification_wrong_index_1(self):
        # this is proof for hello1
        value = 'hello1'
        correct_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 1, correct_proof, root_value)
        self.assertFalse(result)

    def test_proof_verification_wrong_index_2(self):
        # this is proof for hello1
        value = 'hello1'
        correct_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 3, correct_proof, root_value)
        self.assertFalse(result)

    def test_proof_verification_wrong_proof(self):
        value = 'hello1'
        # this is a proof that should not pass verification
        a_wrong_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', '00000']
        root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        result = merkle_tree.verify_proof(value, 0, a_wrong_proof, root_value)
        self.assertFalse(result)

    def test_calculate_proof(self):
        values = ['hello1', 'hello2', 'hello3', 'hello4']
        m_t = merkle_tree.MerkleTree(values)
        proof = m_t.calculate_proof(0)
        correct_proof = ['87298cc2f31fba73181ea2a9e6ef10dce21ed95e98bdac9c4e1504ea16f486e4', 'a39eedabc3374c61cadd2d9629048fff66df3278d4bdd439011d6a3caf1671d9']
        self.assertEqual(proof, correct_proof)

    def test_create_proof_and_verify(self):
        values = ['hello1', 'hello2', 'hello3', 'hello4']
        m_t = merkle_tree.MerkleTree(values)
        root = m_t.root.value
        for i in range(len(values)):
            proof = m_t.calculate_proof(i)
            result = merkle_tree.verify_proof(values[i], i, proof, root)
            self.assertTrue(result)

    def test_add_value_1(self):
        values = ['hello1', 'hello2', 'hello3']
        expected_root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        m_t = merkle_tree.MerkleTree(values)
        m_t.add_value('hello4')
        self.assertEqual(m_t.root.value, expected_root_value)

    def test_add_value_2(self):
        values = ['hello1', 'hello2']
        expected_root_value = 'f357c285de34fd9093f85375744796e809f587195b7fe23c428ec09dba08ac95'
        m_t = merkle_tree.MerkleTree(values)
        m_t.add_value('hello3')
        self.assertEqual(m_t.root.value, expected_root_value)

    def test_concat(self):
        values = ['hello1', 'hello2', 'hello3', 'hello4']
        m_t_1 = merkle_tree.MerkleTree(values[:2])
        m_t_2 = merkle_tree.MerkleTree(values[2:])
        m_t_1.concat(m_t_2)
        expected_root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        self.assertEqual(m_t_1.root.value, expected_root_value)

    def test_update_value_at_index(self):
        values = ['hello1', 'hello2', 'foo', 'hello4']
        m_t = merkle_tree.MerkleTree(values)
        m_t.update_value_at_index(2, 'hello3')
        expected_new_values = ['hello1', 'hello2', 'hello3', 'hello4']
        expected_root_value = '1e278a276e6a4fa4a18754410f165207e6f83d5d407389458a0409ac82fcb834'
        self.assertEqual(m_t.values, expected_new_values)
        self.assertEqual(m_t.root.value, expected_root_value)

    def test_update_value_at_index_error(self):
        with self.assertRaises(IndexError):
            values = ['hello1', 'hello2', 'hello3', 'hello4']
            m_t = merkle_tree.MerkleTree(values)
            m_t.update_value_at_index(5, 'bar')


if __name__ == '__main__':
    unittest.main()
    

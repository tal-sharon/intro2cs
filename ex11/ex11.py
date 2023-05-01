import copy
import itertools as it
POSITIVE = 0
NEGATIVE = 1


class Node:
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child


class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms


def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records
		
		
class Diagnoser:
	def __init__(self, root):
		self.root = root
		
	def diagnose(self, symptoms):
		cur_node = self.root
		while cur_node:
			if not (cur_node.negative_child or cur_node.positive_child):
				# if children are None, Node is a leaf -> therefore, return it's data.
				return cur_node.data
			if cur_node.data in symptoms:
				# the answer is yes -> go to positive child
				cur_node = cur_node.positive_child
			else:
				# the answer is no -> go to negative child
				cur_node = cur_node.negative_child
		return None
		
	def calculate_success_rate(self, records):
		if records is None or len(records) == 0:
			raise ValueError("Records list is empty or None")
		success_count = 0
		for record in records:
			symptoms = record.symptoms
			if record.illness == self.diagnose(symptoms):
				success_count += 1
		return success_count / len(records)

	def all_illnesses(self):
		def get_all_leaves(node, ill_dict):
			if node and not (node.negative_child or node.positive_child):
				# if node is a leaf
				illness = node.data
				if not illness:
					# if leaf data is None, don't add to dictionary
					return None
				if illness in ill_dict.keys():
					ill_dict[illness] += 1
				else:
					ill_dict[illness] = 1
				return None
			# if node is not leaf, check negative and positive children.
			if node:
				get_all_leaves(node.negative_child, ill_dict)
				get_all_leaves(node.positive_child, ill_dict)

		illnesses = dict()
		get_all_leaves(self.root, illnesses)
		ill_lst = sorted(illnesses.keys(), key=lambda k: illnesses[k], reverse=True)
		return ill_lst

	def paths_to_illness(self, illness):
		def get_paths(node, paths_lst, path, ill):
			# if node is a leaf
			if not (node.negative_child or node.positive_child):
				if ill == node.data:
					paths_lst.append(path[:])
				return paths_lst
			# if node is not a leaf, get permutations of True or False
			for bool_value in [True, False]:
				if bool_value:
					path.append(bool_value)
					get_paths(node.positive_child, paths_lst, path, ill)
					path.pop()
				else:
					path.append(bool_value)
					get_paths(node.negative_child, paths_lst, path, ill)
					path.pop()
			return paths_lst

		paths = get_paths(self.root, [], [], illness)
		return paths

	def minimize(self, remove_empty=False):

		def get_tree_list(node, tree_lst):
			tree_lst.append(node.data)
			if not (node.negative_child or node.positive_child):
				return tree_lst
			get_tree_list(node.positive_child, tree_lst)
			get_tree_list(node.negative_child, tree_lst)
			return tree_lst

		def find_minimalism(node, suspect=None):
			if not (node.negative_child or node.positive_child):
				return None
			pos_child = get_tree_list(node.positive_child, [])
			neg_child = get_tree_list(node.negative_child, [])
			if pos_child == neg_child:
				suspect = node
				return suspect
			for value in range(2):
				if value == POSITIVE:
					suspect = find_minimalism(node.positive_child)
					if suspect:
						node.positive_child = node.positive_child.positive_child
						break
				if value == NEGATIVE:
					suspect = find_minimalism(node.negative_child)
					if suspect:
						node.negative_child = node.negative_child.negative_child
						break
			return None

		def empty_minimalism(node, suspect=None):
			if not (node.negative_child or node.positive_child):
				return None
			if len(Diagnoser(node.positive_child).all_illnesses()) == 0:
				suspect = POSITIVE
				return suspect
			if len(Diagnoser(node.negative_child).all_illnesses()) == 0:
				suspect = NEGATIVE
				return suspect
			for value in range(2):
				if value == POSITIVE:
					suspect = empty_minimalism(node.positive_child)
					if suspect:
						if suspect == POSITIVE:
							node.positive_child = node.positive_child.negative_child
						else:
							node.positive_child = node.positive_child.positive_child
						break
				if value == NEGATIVE:
					if suspect:
						if suspect == POSITIVE:
							node.positive_child = node.positive_child.negative_child
						else:
							node.positive_child = node.positive_child.positive_child
						break
			return None

		if find_minimalism(self.root) == self.root:
			self.root = self.root.positive_child

		if remove_empty:
			if empty_minimalism(self.root):
				if empty_minimalism(self.root) == POSITIVE:
					self.root = self.root.negative_child
				else:
					self.root = self.root.positive_child
		return None


def build_tree(records, symptoms):
	for record in records:
		if not isinstance(record, Record):
			raise TypeError('An item in records list is not a Record type object')
	for symptom in symptoms:
		if not isinstance(symptom, str):
			raise TypeError("An item in symptoms list is not a string type object")
	if len(symptoms) == 0:
		illness = find_matched_illness(records, symptoms, symptoms)
		return Diagnoser(Node(illness, None, None))
	diagnoser = Diagnoser(helper_build_tree(records, symptoms, symptoms, 0))
	return diagnoser


def helper_build_tree(records, org_symptoms, cur_symptoms, ind):
	if ind == len(cur_symptoms):
		# reached the end of the end of the tree -> add a matching leaf
		illness = find_matched_illness(records, org_symptoms, cur_symptoms)
		if illness:
			return Node(illness, None, None)
		return Node(None, None, None)

	# build tree of positive child with cur symptoms list
	new_symptoms = copy.deepcopy(cur_symptoms)
	pos_child = helper_build_tree(records, org_symptoms, new_symptoms, ind + 1)

	# build tree of negative child with new symptoms list not containing the current symptom
	new_symptoms.remove(cur_symptoms[ind])
	neg_child = helper_build_tree(records, org_symptoms, new_symptoms, ind)

	return Node(cur_symptoms[ind], pos_child, neg_child)


def find_matched_illness(records, org_symptoms, final_symptoms):
	matches = dict()
	for record in records:
		if is_match(final_symptoms, org_symptoms, record):
			if record.illness in matches.keys():
				matches[record.illness] += 1
			else:
				matches[record.illness] = 1
	if len(matches) != 0:
		lst = sorted(matches.keys(), key=lambda k: matches[k], reverse=True)
		matched_illness = lst[0]
		return matched_illness
	# if there are no matches -> return None
	return None


def is_match(final_symptoms, org_symptoms, record):
	if len(org_symptoms) == 0:
		return True
	if len(final_symptoms) == 0 and record.symptoms is not None:
		# TODO when running diagnoser - returns healthy although there are symptoms in checked diagnose (func) symptoms list
		if len(record.symptoms) == 0:
			return True
		return False
	for symptom in final_symptoms:
		if symptom not in record.symptoms:
			return False
	if record.symptoms:
		for symptom in record.symptoms:
			if symptom in org_symptoms and symptom not in final_symptoms:
				return False
	return True


def optimal_tree(records, symptoms, depth):
	# check for exceptions
	if 0 > depth:
		raise ValueError("Depth can't be negative")
	elif len(symptoms) < depth:
		raise ValueError("Depth can't be bigger than length of symptoms list")
	if len(symptoms) != len(set(symptoms)):
		raise ValueError("Symptoms list can't contain a certain symptom more than once")
	for record in records:
		if not isinstance(record, Record):
			raise TypeError("An item in records list is not a Record type object")
	for symptom in symptoms:
		if not isinstance(symptom, str):
			raise TypeError("An item in symptoms list is not a string type object")

	tree_dict = dict()
	for symp_lst in it.combinations(symptoms, depth):
		diagnoser = build_tree(records, list(symp_lst))
		tree_dict[symp_lst] = diagnoser.calculate_success_rate(records)
	ranked_trees = sorted(tree_dict, key=lambda k: tree_dict[k])
	opt_tree = build_tree(records, list(ranked_trees[-1]))
	return opt_tree


if __name__ == "__main__":
	pass

	# Manually build a simple tree.
	#                cough
	#          Yes /       \ No
	#        fever           healthy
	#   Yes /     \ No
	# covid-19   cold

	# flu_leaf = Node("covid-19", None, None)
	# cold_leaf = Node("cold", None, None)
	# inner_vertex = Node("fever", flu_leaf, cold_leaf)
	# healthy_leaf = Node("healthy", None, None)
	# root = Node("cough", inner_vertex, healthy_leaf)
	#
	# diagnoser = Diagnoser(root)
	#
	# # Simple test
	# diagnosis = diagnoser.diagnose(["cough"])
	# if diagnosis == "cold":
	# 	print("Test passed")
	# else:
	# 	print("Test failed. Should have printed cold, printed: ", diagnosis)

# Add more tests for sections 2-7 here.

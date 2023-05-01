# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# Manually build a simple tree.
#                cough
#          Yes /       \ No
#        fever           healthy
#   Yes /     \ No
# covid-19   cold
#
# covid_leaf = Node("covid-19", None, None)
# cold_leaf = Node("cold", None, None)
# healthy_leaf = Node("healthy", None, None)
# inner_vertex1 = Node("fever", covid_leaf, cold_leaf)
# inner_vertex2 = Node("fever", covid_leaf, cold_leaf)
# headache2 = Node("headache", inner_vertex2, healthy_leaf)
# headache1 = Node("headache", inner_vertex1, inner_vertex2)
# root_1 = Node("cough", headache1, headache2)
# diagnoser_1 = Diagnoser(root_1)
# headache_1 = Node('headache', covid_leaf, cold_leaf)
# headache_2 = Node('headache', cold_leaf, healthy_leaf)
# Diagnoser(Node('cough',
# 			   Node('headache', Node('cold', None, None),
# 					Node('sore_throat', Node('covid', None, None), Node('covid', None, None))),
# 			   Node('sore_throat', Node(None, None, None), Node(None, None, None)))).minimize(True)
# root_2 = Node('cough', headache_1, headache_2)
# diagnoser_2 = Diagnoser(root_2)
#
# # # Simple test
# # diagnosis = diagnoser_1.diagnose(["cough"])
# # if diagnosis == "cold":
# # 	print("Test passed")
# # else:
# # 	print("Test failed. Should have printed cold, printed: ", diagnosis)
# #
# # # Test calculate_success_rate
# # recs = parse_data("tiny_data.txt")
# # rate = diagnoser_1.calculate_success_rate(recs)
# # print(rate)
# #
# # # Test all_illnesses
# # illness_dict = diagnoser_2.all_illnesses()
# # print(illness_dict)
# #
# # # Test paths_to_illness
# # paths_list = diagnoser_2.paths_to_illness('cold')
# # print(paths_list)
#
# Test build_tree
# recs = parse_data("tiny_data.txt")
# print()
# for rec in recs:
# 	print('illness:', rec.illness, ' symptoms:', rec.symptoms)
# print()
# symptoms_lst = ['fever', 'cough', 'sore_throat']
# diagnoser_3 = build_tree(recs, symptoms_lst)
# print(diagnoser_3.minimize())
# diagnosis_3 = diagnoser_3.diagnose(['internal_bleed', 'cough'])
# all_ill_lst = diagnoser_3.all_illnesses()
# #
# #
# # print(all_ill_lst)
# # print('diagnosis is:', diagnosis_3)
# #
# # print()
# opt_diagnoser = optimal_tree(recs, symptoms_lst, 0)
# print(opt_diagnoser.all_illnesses())
# print(opt_diagnoser.calculate_success_rate(recs))
# print(opt_diagnoser.paths_to_illness('cold'))
# print(opt_diagnoser.diagnose(['sore_throat']))
#
#
# # Add more tests for sections 2-7 here.

# project_path = r'C:\devel\IRLM-dataset'
# assets_path = project_path + r'\pipeline\assets'
# B_search_queries_path = assets_path + r'\B_search_queries.json'
# C_search_queries_path = assets_path + r'\C_search_queries.json'
# C_search_queries_list_path = assets_path + r'\C_search_queries_list.json'
# D_search_result_folder_path = assets_path + r'\D_search_results\D_search_result.json'
# D_final_search_result_path = assets_path + r'\D_search_result.json'
# E_filter_results_folder_path = assets_path + r'\E_filter_result\E_filter_result.json'
# D_aggregated_search_result_folder_path = assets_path + r'\D_search_results\D_search_result-aggregated-10.json'
# E_filter_results_path = assets_path + r'\E_filter_result.json'
# F_filter_results_path = assets_path + r'\F_filter_result.json'
# original_MAGPIE_dataset = assets_path + r'\MAGPIE_unfiltered.jsonl.txt'
# MAGPIE_dataset = assets_path + r'\MAGPIE_dataset.json'

import os

project_path = os.getcwd()
assets_path = os.path.join(project_path, 'pipeline', 'assets')

# Search query paths
B_search_queries_path = os.path.join(assets_path, 'B_search_queries.json')
C_search_queries_path = os.path.join(assets_path, 'C_search_queries.json')
C_search_queries_list_path = os.path.join(assets_path, 'C_search_queries_list.json')

# Search result paths
D_search_result_folder_path = os.path.join(assets_path, 'D_search_results', 'D_search_result.json')
D_final_search_result_path = os.path.join(assets_path, 'D_search_result.json')
D_aggregated_search_result_folder_path = os.path.join(assets_path, 'D_search_results', 'D_search_result-aggregated-10.json')

# Filter result paths
E_filter_results_path = os.path.join(assets_path, 'E_filter_result', 'E_filter_result.json')
# E_filter_results_path = os.path.join(assets_path, 'E_filter_result.json')
F_filter_results_path = os.path.join(assets_path, 'F_filter_result.json')

# Dataset paths
original_MAGPIE_dataset = os.path.join(assets_path, 'MAGPIE_unfiltered.jsonl.txt')
MAGPIE_dataset = os.path.join(assets_path, 'MAGPIE_dataset.json')

#chromedriver paths
chromedriver_path = os.path.join(project_path, 'pipeline', 'chromedriver-linux64', 'chromedriver')
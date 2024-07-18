def find_value(matrix, value):
    indices = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == value:
                indices.append((i, j))
    return indices

def categorize_results(indices):
    categories = {0: [], 1: [], 2: [], 3: []}
    for row, col in indices:
        categories[col].append((row, col))
    return categories

def process_matrix(matrix, value):
    # Using the function to find the value in the matrix
    result = find_value(matrix, value)

    # Categorize and print the results
    categorized_results = []
    if result:
        categorized_results = categorize_results(result)
        print(f"The value {value} is present at the following indices:")
        for index in result:
            print(index)
        print("\nCategorized indices:")
        for category, indices in categorized_results.items():
            print(f"Category {category}:")
            for index in indices:
                print(index)
    else:
        print(f"The value {value} is not present in the matrix.")

    return categorized_results

# Example matrix setup
def Categorized_Value():
    matrix = input("please input matrix here and enter an empty line in the end: \n")

    while True:
        temp = input("")
        if not temp:
            break
        matrix += temp
        temp = ""

    import re
    matrix = re.sub(r'\s+', ' ', matrix).replace(' ', ',').replace(';','')
    import json
    matrix = json.loads(matrix)
    # print(matrix)

    # The value to find in the matrix
    value = 1

    # Process the matrix to find the value and categorize results
    return process_matrix(matrix, value)

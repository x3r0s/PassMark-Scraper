import os
import csv
import json
import requests
from bs4 import BeautifulSoup

# 1. Create 'data' directory in the current script's location
output_dir = os.path.join(os.getcwd(), 'data')
os.makedirs(output_dir, exist_ok=True)

# 2. Fetch data (parsing from URL)
url = 'https://www.cpubenchmark.net/cpu_list.php'
response = requests.get(url)

if response.status_code != 200:
    print(f"Error: Unable to fetch data from {url}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# 3. Parse data (CPU name, PassMark score, Rank, Value)
cpu_data_list = []
cpu_table = soup.find('table', {'id': 'cputable'})
rows = cpu_table.find('tbody').find_all('tr')

for row in rows:
    columns = row.find_all('td')
    
    if len(columns) >= 4:
        cpu_name = columns[0].get_text(strip=True)
        
        # Remove commas and convert score/rank to int
        cpu_mark = columns[1].get_text(strip=True).replace(",", "")
        cpu_rank = columns[2].get_text(strip=True).replace(",", "")
        
        # For cpu_value, remove commas and convert to float
        cpu_value = columns[3].get_text(strip=True).replace(",", "")
        
        # Convert 'NA' values to None (NULL in SQL)
        cpu_mark = None if cpu_mark == 'NA' else int(cpu_mark)  # Convert to integer
        cpu_rank = None if cpu_rank == 'NA' else int(cpu_rank)  # Convert to integer
        cpu_value = None if cpu_value == 'NA' else float(cpu_value)  # Convert to float

        # Add data to the list
        cpu_data_list.append({
            'cpu_name': cpu_name,
            'passmark_score': cpu_mark,
            'passmark_rank': cpu_rank,
            'passmark_value': cpu_value
        })

# 4. Separate each file saving method into a function

def save_to_csv(data_list):
    csv_file_path = os.path.join(output_dir, 'data.csv')
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['cpu_name', 'passmark_score', 'passmark_rank', 'passmark_value'])
        writer.writeheader()
        writer.writerows(data_list)
    print(f"CSV file saved to {csv_file_path}")

def save_to_json(data_list):
    json_file_path = os.path.join(output_dir, 'data.json')
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)
    print(f"JSON file saved to {json_file_path}")

def save_to_sql(data_list):
    sql_file_path = os.path.join(output_dir, 'data.sql')
    with open(sql_file_path, mode='w', encoding='utf-8') as sql_file:
        sql_file.write("BEGIN TRANSACTION;\n")
        for cpu in data_list:
            sql_file.write(f"INSERT INTO cpu_benchmark (cpu_name, passmark_score, passmark_rank, passmark_value) "
                           f"VALUES ('{cpu['cpu_name']}', {cpu['passmark_score'] if cpu['passmark_score'] is not None else 'NULL'}, "
                           f"{cpu['passmark_rank'] if cpu['passmark_rank'] is not None else 'NULL'}, "
                           f"{cpu['passmark_value'] if cpu['passmark_value'] is not None else 'NULL'});\n")
        sql_file.write("COMMIT;\n")
    print(f"SQL file saved to {sql_file_path}")

# 5. User selects the save format
def main():
    print("Choose a format to save the CPU data:")
    print("1: CSV")
    print("2: JSON")
    print("3: SQL")
    print("4: ALL")
    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        save_to_csv(cpu_data_list)
    elif choice == '2':
        save_to_json(cpu_data_list)
    elif choice == '3':
        save_to_sql(cpu_data_list)
    elif choice == '4':
        save_to_csv(cpu_data_list)
        save_to_json(cpu_data_list)
        save_to_sql(cpu_data_list)
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

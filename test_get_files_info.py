from functions import get_file_info

print(get_file_info("calculator", "."))
print(get_file_info("calculator", "/bin"))
print(get_file_info("calculator", "../"))
print(get_file_info("calculator", "main.py"))

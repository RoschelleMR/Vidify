# testing if the videos location is accessible

file_path = 'videos/generated/test.txt'

with open(file_path, 'w') as file:
    file.write('This is a test file.')

print('File created successfully.')
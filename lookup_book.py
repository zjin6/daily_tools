import os
import shutil

books = ["Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",    "Data Wrangling with Python",    "Data Science from Scratch: Second Edition",    "Data Science Project with Python: A Complete Guide",    "Building Machine Learning and Deep Learning Models with TensorFlow",    "Data Science with Python: A Practical Guide",    "Data Science in Action",    "Data Science Fundamentals",    "Python for Data Science Quick Start Guide",    "Python Machine Learning: A Guide for Data Scientists",    "Data Science with Python: A Practical Approach to Scientific Computing and Analysis", 'Python_for_Science']

def find_books(root, books):
    for subdir, dirs, files in os.walk(root):
        for file in files:
            for book in books:
                if book in file:
                    shutil.copy2(os.path.join(subdir, file), os.path.expanduser("~/Desktop/data science books"))
                    print('find book: ', book)
                    books.remove(book)
                    break
    for book in books:
        print(f"{book} not found")

root = r'C:\Users\zjin6\OneDrive - azureford\9 User_zjin6'
find_books(root, books)

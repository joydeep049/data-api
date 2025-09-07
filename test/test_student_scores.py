#!/usr/bin/env python3
# test_student_scores.py - test the student scores functionality with mock data

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from student_scores_simple import StudentScoreProcessor

def test_with_mock_data():
    # test with some mock student data
    print("Testing student scores with mock data...")
    
    # create processor
    processor = StudentScoreProcessor()
    
    # create some mock student data
    mock_students = [
        {'name': 'Alice Johnson', 'score': 85},
        {'name': 'Bob Smith', 'score': 92},
        {'name': 'Carol Davis', 'score': 78},
        {'name': 'David Wilson', 'score': 88},
        {'name': 'Eva Brown', 'score': 95},
        {'name': 'Frank Miller', 'score': 82},
        {'name': 'Grace Lee', 'score': 90},
        {'name': 'Henry Taylor', 'score': 76}
    ]
    
    # calculate average
    average = processor.calculate_average(mock_students)
    
    # display summary
    processor.display_summary(mock_students, average)
    
    # create text chart
    processor.create_text_chart(mock_students, average)
    
    print("\nMock data test complete!")

if __name__ == "__main__":
    test_with_mock_data()
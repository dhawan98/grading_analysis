import os
import re

def extract_scores(file_path, grading_scheme, is_second_directory=False):
    """Extract scores from a magnetar.txt file based on the given grading scheme."""
    scores = {key: 0 for key in grading_scheme.keys()}
    
    # Read file content
    with open(file_path, 'r') as file:
        data = file.read()
    
    # Match and calculate scores
    for component in grading_scheme.keys():
        # Handle EndToEnd scores for the second directory
        if is_second_directory:
            key = f"EndToEnd{component}"
        else:
            key = component
        
        match = re.search(rf"{key}.*?\((\d+)/(\d+)\)", data, re.DOTALL)
        if match:
            obtained, total = map(int, match.groups())
            scores[component] = (obtained / total) * grading_scheme[component]
    
    # Calculate the final score (rounded up to 6 decimal places for accuracy)
    final_score = round(sum(scores.values()), 6)
    return final_score, scores, data

def merge_magnetar_files(main_directory1, main_directory2, grading_scheme1, grading_scheme2):
    """Merge magnetar.txt files for each group and add scores at the top."""
    for group_folder in os.listdir(main_directory2):
        group_path2 = os.path.join(main_directory2, group_folder)
        group_path1 = os.path.join(main_directory1, group_folder)
        
        if os.path.isdir(group_path2):
            magnetar_file2 = os.path.join(group_path2, "magnetar.txt")
            magnetar_file1 = os.path.join(group_path1, "magnetar.txt")
            
            if os.path.exists(magnetar_file2) and os.path.exists(magnetar_file1):
                # Extract scores and content
                score1, scores1, content1 = extract_scores(magnetar_file1, grading_scheme1, is_second_directory=False)
                score2, scores2, content2 = extract_scores(magnetar_file2, grading_scheme2, is_second_directory=True)
                total_score = round(score1 + score2, 6)
                
                # Prepare merged content
                merged_content = (
                    f"Scores:\n"
                    f"Out of 45: {round(score1, 2):.2f}\n"
                    f"Out of 5: {round(score2, 2):.2f}\n"
                    f"Total (Out of 50): {round(total_score, 2):.2f}\n\n"
                    "Merged Content:\n"
                    + content1
                    + "\n\n"
                    + content2
                )
                
                # Write the merged content to the second directory's magnetar.txt
                with open(magnetar_file2, "w") as merged_file:
                    merged_file.write(merged_content)
                print(f"Merged and updated {magnetar_file2}.")

def main():
    # Directory 1: Main directory with all components contributing to 45 points
    main_directory1 = "/Users/aashishdhawan/Downloads/Magnetar/submissions/final-evaluation-final/online"
    grading_scheme1 = {
        "Lexer": 6,
        "Parser": 11,
        "Interpreter": 11,
        "Analyzer": 11,
        "Generator": 6
    }
    
    # Directory 2: Directory with Interpreter and Generator contributing to 5 points
    main_directory2 = "/Users/aashishdhawan/Downloads/Magnetar/submissions/end-to-end-final/online"
    grading_scheme2 = {
        "Interpreter": 2.5,
        "Generator": 2.5
    }
    
    # Merge files and update magnetar.txt
    merge_magnetar_files(main_directory1, main_directory2, grading_scheme1, grading_scheme2)

if __name__ == "__main__":
    main()

# Python script to read and extract individual scores from a file and output to a text file

def read_scores_from_file(filename):
    scores_data = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Process the second line to get headers
        headers_line = lines[1].strip()  # The second line contains the header (after "SCORE:")
        headers = headers_line.split()[1:-1]  # Skip the first "SCORE:" label and the last "description"
        
        # Process each subsequent line that starts with "SCORE:"
        for line in lines[2:]:  # Start from the third line onward
            line = line.strip()
            if line.startswith("SCORE:"):  # Only process lines that start with SCORE:
                # Split the line by whitespace and extract the scores
                parts = line.split()
                scores = parts[1:-1]  # Skip the first "SCORE:" label and the last description field
                scores = [float(score) for score in scores]  # Convert scores to float
                
                # Append the scores for each row (with the sequence name at the end)
                sequence_name = parts[-1]  # Last element is the sequence/description
                scores_data.append((scores, sequence_name))
    
    return headers, scores_data


def sort_and_write_scores_to_file(headers, scores_data, output_filename):
    with open(output_filename, 'w') as output_file:
        # Write the header line to the output file
        output_file.write(f"{'Score Type':<25} {'Score Value':<15} {'Sequence Name'}\n")
        output_file.write('-' * 65 + '\n')
        
        # Iterate over each set of scores and sequence name
        for scores, sequence_name in scores_data:
            # Combine the scores with their corresponding headers and sort by score type (header)
            sorted_scores_with_headers = sorted(zip(headers, scores), key=lambda x: x[0])  # Sort by score type
            
            # Write each sorted score and header pair
            for header, score in sorted_scores_with_headers:
                output_file.write(f"{header:<25} {score: .3f} {sequence_name}\n")
            
            # Add a separator line between each row
            output_file.write('-' * 65 + '\n')
        
    print(f"Output has been written to {output_filename}")


def main():
    input_filename = "score.sc"
    output_filename = "extracted_scores.txt"
    
    # Read and extract the headers and individual scores from the file
    headers, scores_data = read_scores_from_file(input_filename)
    
    # Write the sorted scores to the output file
    sort_and_write_scores_to_file(headers, scores_data, output_filename)


if __name__ == "__main__":
    main()

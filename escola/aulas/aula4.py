import logging

# Basic logger configuration
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Add a console handler with custom colored formatting
console_handler = logging.StreamHandler()
formatter = logging.Formatter('\033[1;30m%(asctime)s\033[0m - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def show_message(message, level='INFO'):
    if level == 'DEBUG':
        logger.debug('\033[1;34m%s\033[0m', message)  # Blue for DEBUG
    elif level == 'INFO':
        logger.info('\033[1;32m%s\033[0m', message)   # Green for INFO
    elif level == 'WARNING':
        logger.warning('\033[1;33m%s\033[0m', message)  # Yellow for WARNING
    elif level == 'ERROR':
        logger.error('\033[1;31m%s\033[0m', message)    # Red for ERROR
    elif level == 'CRITICAL':
        logger.critical('\033[1;41m\033[1;37m%s\033[0m', message)  # White on red for CRITICAL
    else:
        logger.info('\033[1;32m%s\033[0m', message)   # Default to green for other levels

# Example usage
show_message("Debug message", 'DEBUG')
show_message("Information message")
show_message("Warning message", 'WARNING')
show_message("Error message", 'ERROR')
show_message("Critical message", 'CRITICAL')

# List of tuples representing the teams' results
results = [
    ("Team A", [10, 15, 20]),
    ("Team B", [12, 18, 24]),
    ("Team C", [8, 16, 24]),
]

# Calculate the average scores for each team
averages = [(team, sum(scores) / len(scores)) for team, scores in results]

# Sort the averages list in descending order
averages = sorted(averages, key=lambda x: x[1], reverse=True)

# Create the ranking list with the team name and its average scores
ranking = [(team, average) for team, average in averages]

# Display the final ranking of the teams
for position, (team, average) in enumerate(ranking, start=1):
    print(f"{position}. {team}: {average:.2f}")
